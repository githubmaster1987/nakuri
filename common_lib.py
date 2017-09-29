import config

import random
import agent
from agent import random_agent
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
from time import sleep
import signal
from proxy_list import random_proxy

def solve_captcha(captcha_site_key, url, logger):
    print(url)
    #
    try:
        s = requests.Session()

        # here we post site key to 2captcha to get captcha ID (and we parse it here too)
        captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(config.captcha_api_key, captcha_site_key, url)).text.split('|')[1]
        # then we parse gresponse from 2captcha response
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(config.captcha_api_key, captcha_id)).text

        print("***********************solving ref captcha************************")

        try_count = 0
        total_count = 0
        while 'CAPCHA_NOT_READY' in recaptcha_answer or 'ERROR_CAPTCHA_UNSOLVABLE' in recaptcha_answer:
            sleep(5)
            #print( "Prev Answer: {}, Call 2Captcha....{}".format(recaptcha_answer, captcha_id))

            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(config.captcha_api_key, captcha_id)).text
           
            if total_count == config.CAPTCHA_ID_CHANGE_MAX_CNT:
                print("Captcha ID count reached at limit value.")
                break

            if try_count == config.CAPTCHA_TRY_MAX_CNT:
                print( "Captcha ID was changed." )
                captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(config.captcha_api_key, captcha_site_key, url)).text.split('|')[1]
                total_count += 1
                try_count = 0

            try_count += 1
        
        if ('CAPCHA_NOT_READY' not in recaptcha_answer) and ('ERROR_CAPTCHA_UNSOLVABLE' not in recaptcha_answer):
            recaptcha_answer = recaptcha_answer.split('|')[1]
            print("^^^^^^^^^^^^^^^^^^^^^^^solved ref captcha^^^^^^^^^^^^^^^^^^^^^^^^^")
        else:
            print("-----------------------not solved ref captcha----------------------")
    except:
        recaptcha_answer = "CAPCHA_NOT_READY"

    return recaptcha_answer

def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension

    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension       

    return str -> plugin_path
    """
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = 'proxy_auth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },

        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def create_firefox_driver():
    try:
        binary = FirefoxBinary("/usr/bin/firefox")
        driver = webdriver.Firefox(firefox_binary=binary)
    except WebDriverException as e:
        print(" WebDriverException -> %s" % str(e))
        return None

    return driver

# @todo https://intoli.com/blog/running-selenium-with-headless-chrome/
def create_chrome_driver(proxy):
    co = Options()
    co.add_argument("--start-maximized")
    co.add_argument('disable-infobars')
    #co.add_argument('headless')
    if proxy is not None:
        proxy_user = ""
        proxy_pwd = ""
        
        if proxy.proxy_auth is not None:
            proxy_user = proxy.proxy_auth.split(':')[0]
            proxy_pwd = proxy.proxy_auth.split(':')[1]
        
        proxyauth_plugin_path = create_proxyauth_extension(
          proxy_host=proxy.host,
          proxy_port=proxy.port,
          proxy_username=proxy_user,
          proxy_password=proxy_pwd
        )
        co.add_extension(proxyauth_plugin_path)

    try:
        driver = webdriver.Chrome(chrome_options=co)
    except WebDriverException as e:
        print(" WebDriverException -> %s" % str(e))

        try:
            if driver:
                phantom_Quit(driver)
        except:
            pass

        return None

    return driver

def create_phantomjs_driver():
    ua = ["D", "W", agent.firefox]

    screen_resolution = [1366, 768] 
    proxy_ip, proxy_port, proxy_user, proxy_pass = random_proxy()

    # agent_str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
    agent_str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    # agent_str = random_agent()[2]
    # print agent_str
    
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = agent_str
    dcap['phantomjs.page.settings.loadImages'] = True
    dcap['phantomjs.page.settings.resourceTimeout'] = 60000

    headers = {
        "Host": "www.naukri.com",
        "User-Agent": agent_str,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    for key, value in enumerate(headers):
        capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
        dcap[capability_key] = value
    
    proxy_str = "{}:{}".format(proxy_ip, proxy_port)
    auth_str = "{}:{}".format(proxy_user, proxy_pass)
    c_type='http'
   
    service_args = ['--proxy=%s' % proxy_str, '--proxy-type=%s' % c_type,'--proxy-auth=%s' % auth_str , '--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false']
    print service_args
    driver = None
    try:
        # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
         # driver = webdriver.PhantomJS()
    except WebDriverException as e:
        print("webdriver.PhantomJS WebDriverException -> %s" % str(e))
        try:
            if driver:
                phantom_Quit(driver)
        except Exception as e:
            pass

        return None

    driver.set_window_size(screen_resolution[0], screen_resolution[1])
    driver.implicitly_wait(config.DRIVER_WAITING_SECONDS)
    driver.set_page_load_timeout(config.DRIVER_WAITING_SECONDS)

    # print driver, ua, proxy_ip, screen_resolution
    return driver
    #return driver, ua, proxy, screen_resolution

def phantom_Quit(driver):
    try:
        driver.close()
    except Exception as e:
        pass
        
    try:
        driver.service.process.send_signal(signal.SIGTERM)
    except Exception as e:
        pass

    try:
        driver.quit()
        del driver
    except Exception as e:
        pass
