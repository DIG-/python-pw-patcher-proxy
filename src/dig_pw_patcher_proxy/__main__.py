import sys

from .arguments import Arguments

arguments = Arguments.parse()
print(arguments)
sys.exit(0)
