import random
import csv
from scrapex import *
from scrapex import common
from scrapex.node import Node
from scrapex.excellib import *
from scrapex.http import Proxy

# now make the request
import socks
import socket
socks.set_default_proxy(socks.SOCKS5, "localhost", 9090)
socket.socket = socks.socksocket

sc_obj = Scraper(
            use_cache=False, #enable cache globally
            retries=3,
            timeout=300,
            )

logger = sc_obj.logger

url = "http://lumtest.com/myip.json"
logger.info("URL: {}".format(url))

# proxy = Proxy("localhost", 9090)
# sc_obj.proxy_manager.session_proxy = proxy

html = sc_obj.load_html(url, use_cache = False)
if html.response.code != 200:
    print html.response.code
logger.info (html)

