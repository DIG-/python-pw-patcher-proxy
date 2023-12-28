import logging


class Log:
    root = logging.getLogger("pw_patcher_proxy")

    @staticmethod
    def get(name: str) -> logging.Logger:
        return Log.root.getChild(name)

    @staticmethod
    def initialize(verbose: int):
        if verbose == 0:
            logging.basicConfig(level=logging.INFO)
        elif verbose >= 1:
            logging.basicConfig(level=logging.DEBUG)
