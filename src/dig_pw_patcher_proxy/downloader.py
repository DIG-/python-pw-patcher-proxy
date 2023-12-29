from .cache import Cache
from .log import Log


class Downloader:
    def __init__(self, cache: Cache, server: str, jobs: int):
        self.cache = cache
        self.server = server
        self.jobs = jobs
        self.log = Log.get("downloader")
