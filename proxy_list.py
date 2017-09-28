import random
import config

def random_proxy():
    proxy_user = config.proxy_username
    proxy_pass = config.proxy_password
    proxy_addr = random.choice(config.proxies)

    proxy_ip = proxy_addr.split(":")[0]
    proxy_port = proxy_addr.split(":")[1]
    return proxy_ip, proxy_port, proxy_user, proxy_pass
