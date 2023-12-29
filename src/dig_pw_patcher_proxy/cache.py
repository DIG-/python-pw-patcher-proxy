from pathlib import Path, PurePath
from shutil import rmtree
from typing import AnyStr
from uuid import uuid4

from .log import Log


class Cache:
    TEMP_DIR = "tmp"

    def __init__(self, path: Path):
        self.log = Log.get("cache")
        self.path = path
        self.log.info("Initialize cache")
        self.log.debug(f"Check if {path.absolute()} exists")
        if not self.path.exists():
            self.log.debug("Creating cache dir")
            self.path.mkdir(parents=True)
        if (self.path / Cache.TEMP_DIR).exists():
            self.log.debug("Clear cache temp dir")
            rmtree(self.path / Cache.TEMP_DIR)
        (self.path / Cache.TEMP_DIR).mkdir()

    def new_temp_file(self) -> Path:
        temp = self.path / Cache.TEMP_DIR / str(uuid4())
        while temp.exists():
            temp = self.path / Cache.TEMP_DIR / str(uuid4())
        return temp

    def move(self, temp: Path, dest: PurePath | AnyStr):
        _dest = self.path / PurePath(dest)
        self.log.debug(f"Moving {temp} to {_dest}")
        if not _dest.parent.exists():
            _dest.parent.mkdir(parents=True)
        temp.rename(_dest)

    def exists(self, filename: PurePath | AnyStr) -> bool:
        return self.get(filename).exists()

    def get(self, filename: PurePath | AnyStr) -> Path:
        return self.path / PurePath(filename)
