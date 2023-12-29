from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from shutil import copyfileobj
from typing import List
from urllib.request import urlopen

from .cache import Cache
from .log import Log


class Downloader:
    CURRENT = "downloader-current"

    def __init__(self, cache: Cache, server: str, jobs: int):
        self.cache = cache
        self.server = server
        self.jobs = jobs
        self.log = Log.get("downloader")
        self.executor: ThreadPoolExecutor | None = None
        self.current: str | None = None
        current = self.cache.get(Downloader.CURRENT)
        if not current.exists():
            return
        version: str | None = None
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
            elif line.startswith("-----"):
                break
            (_, url) = line.split()
            if url.startswith("/"):
                urls.append(url)
                last_url = "/".join(url.split("/")[:-1])
            else:
                urls.append(f"{last_url}/{url}")

        self.executor = ThreadPoolExecutor(max_workers=self.jobs)
        downloads = self.executor.map(self.download, urls)
        self.executor.submit(lambda x: x.restart() if not all(downloads) else None, self)

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
        self.executor = None
        self.current = None

    def download(self, url: str) -> bool:
        path = url[1:]
        if self.cache.exists(path):
            return True
        self.log.debug(f"Caching {url}")
        with urlopen(f"{self.server}element/element/{path}") as response:
            if response.status != HTTPStatus.OK:
                return False
            temp = self.cache.new_temp_file()
            with open(temp, mode="wb") as file:
                copyfileobj(response, file)
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
