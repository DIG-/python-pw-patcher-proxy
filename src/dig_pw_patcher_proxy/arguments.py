from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

__all__ = ["Arguments"]


@dataclass
class Arguments:
    server: str
    cache: Path
    jobs: int
    port: int
    verbose: int

    @staticmethod
    def parse() -> "Arguments":
        parser = ArgumentParser(prog="dig_pw_patcher_proxy", description="PW Patcher Proxy")
        parser.add_argument(
            "-s", "--server", default="http://fpatch3.perfectworld.com.br/CPW/", help="Original patch server url"
        )
        parser.add_argument("-c", "--cache", default="cache", type=Path, help="Directory to cache files")
        parser.add_argument("-j", "--jobs", default=8, type=int, help="Number of parallel cache download")
        parser.add_argument("-p", "--port", default=8080, type=int, help="Port of proxy server")
        parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase log level")
        args = parser.parse_args()
        return Arguments(args.server, args.cache, args.jobs, args.port, args.verbose)
