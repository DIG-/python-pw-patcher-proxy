import sys

from .arguments import Arguments
from .cache import Cache
from .log import Log

arguments = Arguments.parse()
Log.initialize(arguments.verbose)
cache = Cache(arguments.cache)
print(arguments)
sys.exit(0)
