from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from re import search as re_search
from shutil import copyfileobj
from typing import Any
from urllib.request import urlopen

from .cache import Cache
from .downloader import Downloader
from .log import Log


class _Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, cache: Cache, downloader: Downloader, server: str, **kwargs):
        self.cache = cache
        self.downloader = downloader
        self.original_url = server
        self.log = Log.get("proxy")
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: Any):  # pylint: disable=redefined-builtin
        self.log.debug(f"{self.address_string()} - {format % args}")

    def do_GET(self):  # pylint: disable=invalid-name
        path = self.path[1:]
        cached = self.cache.get(path)
        if cached.exists() and not cached.is_dir():
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Length", f"{cached.stat().st_size}")
            self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            with cached.open(mode="rb") as file:
                copyfileobj(file, self.wfile)
            return

        try:
            found = re_search(r"element/(v-[\d]+).inc", path)
            if found:
                self.downloader.start(found.group(1))
            with urlopen(f"{self.original_url}{path}") as content:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/octet-stream")
                self.end_headers()
                copyfileobj(content, self.wfile)
        except BaseException as e:  # pylint: disable=broad-exception-caught
            self.send_error(HTTPStatus.BAD_GATEWAY, explain=str(e))


class Proxy:
    def __init__(self, cache: Cache, downloader: Downloader, server: str, bind: str, port: int):
        self.cache = cache
        self.downloader = downloader
        self.server = server
        self.log = Log.get("proxy")
        self.log.info(f"Initialize server on {bind}:{port}")
        self.daemon = ThreadingHTTPServer(server_address=(bind, port), RequestHandlerClass=self._handler)

    def run(self):
        try:
            self.daemon.serve_forever()
        except KeyboardInterrupt:
            self.log.info("Server stopped by user")
        except:  # pylint: disable=bare-except
            self.log.exception("Server stopped")

    def _handler(self, *args, **kwargs) -> _Handler:
        return _Handler(*args, cache=self.cache, downloader=self.downloader, server=self.server, **kwargs)
