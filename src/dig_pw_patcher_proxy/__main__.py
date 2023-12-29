import sys

from .arguments import Arguments
from .cache import Cache
from .downloader import Downloader
from .log import Log
from .proxy import Proxy

arguments = Arguments.parse()
Log.initialize(arguments.verbose)
cache = Cache(path=arguments.cache)
downloader = Downloader(cache=cache, server=arguments.server, jobs=arguments.jobs)
proxy = Proxy(cache=cache, downloader=downloader, server=arguments.server, bind=arguments.bind, port=arguments.port)
proxy.run()
downloader.stop()
sys.exit(0)
