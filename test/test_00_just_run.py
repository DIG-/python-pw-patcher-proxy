from dig_pw_patcher_proxy.arguments import Arguments
from dig_pw_patcher_proxy.cache import Cache
from dig_pw_patcher_proxy.downloader import Downloader
from dig_pw_patcher_proxy.log import Log
from dig_pw_patcher_proxy.proxy import Proxy


def test_just_run():
    arguments = Arguments.default()
    arguments.verbose = 99
    Log.initialize(arguments.verbose)
    cache = Cache(path=arguments.cache)
    downloader = Downloader(cache=cache, server=arguments.server, jobs=arguments.jobs)
    Proxy(cache=cache, downloader=downloader, server=arguments.server, bind=arguments.bind, port=arguments.port)
    downloader.stop()
