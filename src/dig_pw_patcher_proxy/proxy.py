from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .cache import Cache
from .downloader import Downloader
from .log import Log


class _Handler(BaseHTTPRequestHandler):
    pass


class Proxy:
    def __init__(self, cache: Cache, downloader: Downloader, server: str, port: int):
        self.cache = cache
        self.downloader = downloader
        self.server = server
        self.port = port
        self.log = Log.get("proxy")
        self.log.info(f"Initialize server on 127.0.0.1:{port}")
        self.daemon = ThreadingHTTPServer(server_address=("127.0.0.1", port), RequestHandlerClass=_Handler)

    def run(self):
        self.daemon.serve_forever()
