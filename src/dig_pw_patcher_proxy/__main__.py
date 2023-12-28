import sys

from .arguments import Arguments
from .log import Log

arguments = Arguments.parse()
Log.initialize(arguments.verbose)
print(arguments)
sys.exit(0)
