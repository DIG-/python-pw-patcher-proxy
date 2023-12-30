from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir

__all__ = ["Arguments"]


@dataclass
class Arguments:
    server: str
    cache: Path
    jobs: int
    bind: str
    port: int
    verbose: int
    clear_cache: bool

    @staticmethod
    def parse() -> "Arguments":
        default = Arguments.default()
        parser = ArgumentParser(prog="dig_pw_patcher_proxy", description="PW Patcher Proxy")
        parser.add_argument("-s", "--server", default=default.server, help="Original patch server url")
        parser.add_argument("-c", "--cache", default=default.cache, type=Path, help="Directory to cache files")
        parser.add_argument("--clear-cache", action="store_true", help="Clear entire cache before start")
        parser.add_argument("-j", "--jobs", default=default.jobs, type=int, help="Number of parallel cache download")
        parser.add_argument("--bind", default=default.bind, type=str, help="Bind proxy server to")
        parser.add_argument("-p", "--port", default=default.port, type=int, help="Port of proxy server")
        parser.add_argument("-v", "--verbose", action="count", default=default.verbose, help="Increase log level")
        args = parser.parse_args()
        return Arguments(args.server, args.cache, args.jobs, args.bind, args.port, args.verbose, args.clear_cache)

    @staticmethod
    def default() -> "Arguments":
        return Arguments(
            server="http://fpatch3.perfectworld.com.br/CPW/",
            cache=Path(gettempdir()) / "pw_patcher_proxy",
            jobs=16,
            bind="127.0.0.1",
            port=8080,
            verbose=0,
            clear_cache=False,
        )
