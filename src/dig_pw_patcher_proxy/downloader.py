from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from http.client import HTTPConnection, HTTPSConnection
from queue import Empty, Full, LifoQueue
from shutil import copyfileobj
from typing import List, Optional
from urllib.request import urlopen

from .cache import Cache
from .log import Log


class _ConnectionPool:
    def __init__(self, secure: bool, host: str, size: int):
        self.size = size + 2
        self.secure = secure
        self.host = host
        self.stack: LifoQueue[HTTPConnection] = LifoQueue(maxsize=self.size)

    def start(self):
        try:
            while True:
                self.release(None, False)
        except Full:
            pass

    def stop(self):
        try:
            while True:
                connection = self.get(False)
                connection.close()
        except Empty:
            pass

    def get(self, block: bool = True) -> HTTPConnection:
        return self.stack.get(block=block)

    def release(self, connection: Optional[HTTPConnection], block: bool = True):
        if not connection:
            if self.secure:
                connection = HTTPSConnection(self.host)
            else:
                connection = HTTPConnection(self.host)
        self.stack.put(connection, block=block)


class Downloader:
    CURRENT = "downloader-current"
    PREFIX = "element/element/"

    def __init__(self, cache: Cache, server: str, jobs: int):
        self.cache = cache
        self.server = server
        self.host = server.split("/")[2]
        self.path = "/" + "/".join(server.split("/")[3:])
        if not self.path.endswith("/"):
            self.path = self.path + "/"
        self.jobs = jobs
        self.log = Log.get("downloader")
        self.connections = _ConnectionPool(server.startswith("https"), self.host, self.jobs)
        self.executor: Optional[ThreadPoolExecutor] = None
        self.current: Optional[str] = None
        current = self.cache.get(Downloader.CURRENT)
        if not current.exists():
            return
        version: Optional[str] = None
        with open(current, mode="r", encoding="utf-8") as file:
            version = file.read()
        if version:
            self.start(version)

    def start(self, version: str):
        if version == self.current:
            return
        self.stop()
        self.log.debug(f"Getting version update {version}")
        with urlopen(f"{self.server}element/{version}.inc") as response:
            if response.status != HTTPStatus.OK:
                self.log.error("Failed to get update file from server")
                return
            content: str = response.read().decode("utf-8")
        with open(self.cache.get(Downloader.CURRENT), mode="w", encoding="utf-8") as file:
            file.write(version)
        self.current = version
        self.log.info(f"Start caching update {version}")
        urls: List[str] = []
        last_url = ""
        for line in content.splitlines():
            if line.startswith("#"):
                continue
            if line.startswith("-----"):
                break
            (_, url) = line.split()
            if url.startswith("/"):
                urls.append(url)
                last_url = "/".join(url.split("/")[:-1])
            else:
                urls.append(f"{last_url}/{url}")

        self.connections.start()
        self.executor = ThreadPoolExecutor(max_workers=self.jobs)
        downloads = self.executor.map(self.download, urls)
        self.executor.submit(lambda x: x.restart() if not all(downloads) else x.complete(), self)

    def restart(self):
        if not self.current:
            self.log.error("Can not restart download")
            return
        self.log.warning("Restart cache due to missing files")
        self.start(self.current)

    def stop(self):
        if not self.executor:
            return
        self.log.info("Stopping downloader")
        self.executor.shutdown(wait=True, cancel_futures=True)
        self.connections.stop()
        self.executor = None
        self.current = None

    def complete(self):
        self.log.info("Caching completed")
        self.connections.stop()
        self.current = None
        self.cache.get(Downloader.CURRENT).unlink()

    def download(self, url: str) -> bool:
        path = Downloader.PREFIX + url[1:]
        if self.cache.exists(path):
            return True
        self.log.debug(f"Caching {url}")
        connection = self.connections.get()
        connection.request("GET", f"{self.path}{path}", headers={"Host": self.host, "Accept": "*/*"})
        response = connection.getresponse()
        if response.status != HTTPStatus.OK:
            response.close()
            self.connections.release(connection)
            return False
        temp = self.cache.new_temp_file()
        with open(temp, mode="wb") as file:
            copyfileobj(response, file)
        self.connections.release(connection)
        self.cache.move(temp, path)
        return True


# GET /element/version
# GET /element/v-2.inc
# GET /element/element/ZGF0YQ==/Z3Nob3AuZGF0YQ==
#
# v-*.inc file:
# # v-from v-to bytes
# !hash /absolute/path/to/file
# !hash relative/to/last/file
# !hash /new/absolute/file
# -----BEGIN ELEMENT SIGNATURE-----
