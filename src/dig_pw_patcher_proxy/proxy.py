from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

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
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Length", "0")
        self.end_headers()


class Proxy:
    def __init__(self, cache: Cache, downloader: Downloader, server: str, port: int):
        self.cache = cache
        self.downloader = downloader
        self.server = server
        self.port = port
        self.log = Log.get("proxy")
        self.log.info(f"Initialize server on 127.0.0.1:{port}")
        self.daemon = ThreadingHTTPServer(server_address=("127.0.0.1", port), RequestHandlerClass=self._handler)

    def run(self):
        self.daemon.serve_forever()

    def _handler(self, *args, **kwargs) -> _Handler:
        return _Handler(*args, cache=self.cache, downloader=self.downloader, server=self.server, **kwargs)
