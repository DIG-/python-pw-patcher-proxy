import sys

from .arguments import Arguments
from .cache import Cache
from .downloader import Downloader
from .log import Log

arguments = Arguments.parse()
Log.initialize(arguments.verbose)
cache = Cache(path=arguments.cache)
downloader = Downloader(cache=cache, server=arguments.server, jobs=arguments.jobs)
print(arguments)
sys.exit(0)
