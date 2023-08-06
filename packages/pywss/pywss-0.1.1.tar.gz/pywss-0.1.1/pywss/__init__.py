# coding: utf-8
import os, re
import json
import time
import signal
import atexit
import loggus
import socket
import threading
import selectors

from _io import BufferedReader
from datetime import timedelta
from pywss.headers import *
from pywss.statuscode import *
from pywss.websocket import WebsocketContextWrap
from pywss.static import NewStaticHandler

__version__ = '0.1.1'


class _Run:
    running = True

    @classmethod
    def stop(cls):
        cls.running = False


signal.signal(signal.SIGTERM, lambda *args: _Run.stop())
signal.signal(signal.SIGINT, lambda *args: _Run.stop())
signal.signal(signal.SIGILL, lambda *args: _Run.stop())
atexit.register(lambda: _Run.stop())


class Context:
    _handler_index = 0
    _flush_header = False

    def __init__(self, fd, r, method, path, version, headers, route, handlers, address):
        self.fd = fd
        self.rfd = r
        self.method = method
        self.version = version
        self.headers = headers
        self.cookies = parse_cookies(headers)
        self.path = path
        self.params = parse_params(path)
        self.route = route
        self._handlers = handlers
        self.address = address
        self.log: loggus.Entry = None

        self.content_length = int(headers.get("Content-Length", 0))
        self.content = b""
        if self.content_length:
            self.content = r.read(self.content_length)

        self.response_status_code = 200
        self.response_headers = {
            "Server": "Pywss",
            "PywssVersion": __version__,
        }
        self.response_body = []

    def next(self):
        if self._handler_index >= len(self._handlers):
            return
        index = self._handler_index
        self._handler_index += 1
        self._handlers[index](self)

    def json(self):
        resp = {}
        try:
            ct = self.headers.get("Content-Type").strip()
            if not ct.startswith("application/json"):
                return resp
            resp = json.loads(self.content.decode())
        except:
            pass
        return resp

    def form(self):
        resp = {}
        try:
            ct = self.headers.get("Content-Type").strip()
            if not ct.startswith("multipart/form-data"):
                return resp
            boundary = ""
            for v in ct.split(";"):
                v = v.strip()
                if v.startswith("boundary="):
                    boundary = v.replace("boundary=", "")
            if not boundary:
                return resp
            for data in self.content.decode().split(f"--{boundary}"):
                data = data.strip()
                if not data.startswith("Content-Disposition"):
                    continue
                h, v = data.split("\r\n\r\n", 1)
                name = re.search("name=\"(.*?)\"", h).group(1)
                resp[name] = v
        except:
            pass
        return resp

    def body(self):
        return self.content.decode()

    def set_header(self, k, v):
        header = []
        for key in k.split("-"):
            header.append(key[0].upper() + key[1:].lower())
        self.response_headers["-".join(header)] = v

    def set_content_type(self, v):
        self.response_headers.setdefault("Content-Type", v)

    def set_cookie(self, key, value, maxAge=None, expires=None, path="/", domain=None, secure=False, httpOnly=False):
        buf = [f"{key}={value}"]
        if isinstance(maxAge, timedelta):
            maxAge = (maxAge.days * 60 * 60 * 24) + maxAge.seconds
        if expires is not None:
            expires = time.gmtime(expires)
        elif maxAge is not None:
            expires = time.gmtime(time.time() + maxAge)
        if expires:
            d = expires
            expires = "%s, %02d%s%s%s%04d %02d:%02d:%02d GMT" % (
                ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[d.tm_wday],
                d.tm_mday,
                "-",
                (
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                )[d.tm_mon - 1],
                "-",
                d.tm_year,
                d.tm_hour,
                d.tm_min,
                d.tm_sec,
            )

        for k, v, q in (
                ("Domain", domain, True),
                ("Expires", expires, False),
                ("Max-Age", maxAge, False),
                ("Secure", secure, None),
                ("HttpOnly", httpOnly, None),
                ("Path", path, False),
        ):
            if q is None:
                if v:
                    buf.append(k)
                continue
            if v is None:
                continue
            buf.append(f"{k}={v}")
        self.response_headers["Set-Cookie"] = "; ".join(buf)

    def set_status_code(self, status_code):
        self.response_status_code = status_code

    def redirect(self, url, status_code=StatusFound):
        self.set_status_code(status_code)
        self.set_header("Location", url)

    def write(self, body):
        if isinstance(body, (str, bytes)):
            self.write_text(body)
        elif isinstance(body, (dict, list)):
            self.write_json(body)
        elif isinstance(body, BufferedReader):
            self.write_file(body)

    def write_text(self, data: str):
        self.set_content_type("text/html; charset=utf-8")
        self.response_body.append(data)

    def write_json(self, data):
        self.set_content_type("application/json")
        self.response_body.append(json.dumps(data, ensure_ascii=False))

    def write_file(self, file):
        if isinstance(file, str) and os.path.exists(file):
            self.response_body.append(open(file, "rb"))
        elif isinstance(file, BufferedReader):
            self.response_body.append(file)

    def ws_read(self):
        raise NotImplementedError

    def ws_write(self, body):
        raise NotImplementedError

    def flush(self):
        if not self._flush_header:
            data = [f"{self.version} {self.response_status_code} Pywss"]
            for k, v in self.response_headers.items():
                data.append(f"{k}: {v}")
            data = "\r\n".join(data) + "\r\n\r\n"
            self.fd.sendall(data.encode())
            self._flush_header = True
        for body in self.response_body:
            if isinstance(body, bytes):
                self.fd.sendall(body)
            elif isinstance(body, str):
                self.fd.sendall(body.encode())
            elif isinstance(body, BufferedReader):
                chunk = body.read(8192)
                while chunk:
                    self.fd.sendall(chunk)
                    chunk = body.read(8192)
                body.close()
        self.response_body = []


class App:

    def __init__(self, base_route="", base_handlers=None):
        self.base_route = f"/{base_route.strip().strip('/')}" if base_route else base_route
        self.base_handlers = list(base_handlers) if base_handlers else []
        self.head_match_routes = []
        self.full_match_routes = {}
        self.log = loggus.GetLogger()

    def register(self, method, route, handlers):
        route = f"/{route.strip().strip('/')}" if route else route
        self.full_match_routes[f"{method}{self.base_route}{route}"] = list(self.base_handlers) + list(handlers)

    def build(self):
        routes = {}
        for route, v in self.full_match_routes.items():
            if isinstance(v, App):
                v.build()
                routes.update(v.full_match_routes)
                self.head_match_routes += v.head_match_routes
            elif route.endswith("*"):
                match = route.strip().rstrip("/*").rstrip("*")
                self.head_match_routes.append((match, v))
                self.log.update({
                    "type": "headmatch",
                    "route": route,
                    "handlers": [handler.__name__ for handler in v],
                }).info(f"bind route")
            else:
                routes[route] = v
                self.log.update({
                    "type": "fullmatch",
                    "route": route,
                    "handlers": [handler.__name__ for handler in v],
                }).info(f"bind route")
        self.full_match_routes = routes

    def party(self, route, *handlers):
        route = f"{self.base_route}/{route.strip().strip('/')}"
        self.full_match_routes[f"{route}"] = App(route, list(self.base_handlers) + list(handlers))
        return self.full_match_routes[f"{route}"]

    def use(self, *handlers):
        self.base_handlers += list(handlers)

    def static(self, route, rootDir, *handlers, staticHandler=NewStaticHandler):
        if staticHandler:
            handlers = list(handlers)
            handlers.append(staticHandler(rootDir))
        if not route.endswith("*"):
            route = f"{route.strip().rstrip('/')}/*"
        self.register("GET", route, handlers)

    def get(self, route, *handlers):
        self.register("GET", route, handlers)

    def post(self, route, *handlers):
        self.register("POST", route, handlers)

    def head(self, route, *handlers):
        self.register("HEAD", route, handlers)

    def put(self, route, *handlers):
        self.register("PUT", route, handlers)

    def delete(self, route, *handlers):
        self.register("DELETE", route, handlers)

    def patch(self, route, *handlers):
        self.register("PATCH", route, handlers)

    def options(self, route, *handlers):
        self.register("OPTIONS", route, handlers)

    def any(self, route, *handlers):
        self.get(route, *handlers)
        self.post(route, *handlers)
        self.head(route, *handlers)
        self.put(route, *handlers)
        self.delete(route, *handlers)
        self.patch(route, *handlers)
        self.options(route, *handlers)

    def _(self, request, address):
        log = self.log
        try:
            r = request.makefile("rb", -1)
            method, path, version, err = parse_request_line(r)
            if err:
                request.sendall(b"HTTP/1.1 404 Pywss\r\n")
                return
            log = log.update(method=method, path=path)
            hes, err = parse_headers(r)
            if err:
                request.sendall(b"HTTP/1.1 404 Pywss\r\n")
                log.error(err)
                return
            # full match
            route = f"{method.upper()}/{path.split('?', 1)[0].strip('/')}"
            handlers = self.full_match_routes.get(route, None)
            # head match
            if not handlers:
                for r, v in self.head_match_routes:
                    if route.startswith(r):
                        route = r
                        handlers = v
            if not handlers:
                request.sendall(b"HTTP/1.1 404 Pywss\r\n")
                log.error("No Handler")
                return
            ctx = Context(request, r, method, path, version, hes, route, handlers, address)
            ctx.log = log
            ctx.next()
            ctx.flush()
        except:
            log.traceback()
        finally:
            request.close()

    def run(self, host="0.0.0.0", port=8080, grace=3, request_queue_size=5, poll_interval=0.5):
        self.build()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(request_queue_size)
        selector = selectors.PollSelector if hasattr(selectors, 'PollSelector') else selectors.SelectSelector
        with self.log.trycache():
            with selector() as _selector:
                _selector.register(sock.fileno(), selectors.EVENT_READ)
                self.log. \
                    update(version=__version__). \
                    variables(host, port, grace). \
                    info("server start")
                while _Run.running:
                    ready = _selector.select(poll_interval)
                    if not ready:
                        continue
                    request, address = sock.accept()
                    threading.Thread(target=self._, args=(request, address)).start()
        time.sleep(grace)
        self.log.panic("server closed")
