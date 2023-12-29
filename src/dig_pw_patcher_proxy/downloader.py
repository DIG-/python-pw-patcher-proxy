from http import HTTPStatus
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
        current = self.cache.get(Downloader.CURRENT)
        if not current.exists():
            return
        version: str | None = None
        with open(current, mode="r", encoding="utf-8") as file:
            version = file.read()
        if version:
            self.start(version)

    def start(self, version: str):
        self.log.debug(f"Getting version update {version}")
        with urlopen(f"{self.server}element/{version}.inc") as response:
            if response.status != HTTPStatus.OK:
                self.log.error("Failed to get update file from server")
                return
            content: str = response.read().decode("utf-8")
        with open(self.cache.get(Downloader.CURRENT), mode="w", encoding="utf-8") as file:
            file.write(version)
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

        for url in urls:
            self.log.debug(f"Url: {url}")


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
