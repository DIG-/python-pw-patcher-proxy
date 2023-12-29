from .cache import Cache
from .log import Log


class Downloader:
    def __init__(self, cache: Cache, server: str, jobs: int):
        self.cache = cache
        self.server = server
        self.jobs = jobs
        self.log = Log.get("downloader")


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
