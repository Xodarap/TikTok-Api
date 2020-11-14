import random
import time
import string
import requests
import logging
from threading import Thread
import time, datetime
import random


# Import Detection From Stealth
from .stealth import stealth
from .get_acrawler import get_acrawler
from playwright import sync_playwright

playwright = None

def get_playwright():
    global playwright
    if playwright == None:
        try:
            playwright = sync_playwright().start()
        except Exception as e:
            raise e
    
    return playwright


class browser:
    def __init__(
        self,
        **kwargs,
    ):
        self.debug = kwargs.get("debug", False)
        self.proxy = kwargs.get("proxy", None)
        self.api_url = kwargs.get("api_url", None)
        self.referrer = kwargs.get("referer", "https://www.tiktok.com/")
        self.language = kwargs.get("language", "en")
        self.executablePath = kwargs.get("executablePath", None)
        self.did = kwargs.get("custom_did", None)
        find_redirect = kwargs.get("find_redirect", False)

        args = kwargs.get("browser_args", [])
        options = kwargs.get("browser_options", {})

        if len(args) == 0:
            self.args = []
        else:
            self.args = args

        self.options = {
            "headless": True,
            "handleSIGINT": True,
            "handleSIGTERM": True,
            "handleSIGHUP": True,
        }

        if self.proxy != None:
            if "@" in self.proxy:
                server_prefix = self.proxy.split("://")[0]
                address = self.proxy.split("@")[1]
                self.options["proxy"] = {
                    "server": server_prefix + "://" + address,
                    "username": self.proxy.split("://")[1].split(":")[0],
                    "password": self.proxy.split("://")[1].split("@")[0].split(":")[1],
                }
            else:
                self.options["proxy"] = {"server": self.proxy}

        self.options.update(options)

        if self.executablePath != None:
            self.options["executablePath"] = self.executablePath

        try:
            self.browser = get_playwright().chromium.launch(args=self.args, **self.options)
        except Exception as e:
            raise e
            logging.critical(e)

        page = self.create_page(set_useragent=True)
        self.get_params(page)
        page.close()

    def get_params(self, page) -> None:
        # self.browser_language = await self.page.evaluate("""() => { return navigator.language || navigator.userLanguage; }""")
        self.browser_language = "en-US"
        # self.timezone_name = await self.page.evaluate("""() => { return Intl.DateTimeFormat().resolvedOptions().timeZone; }""")
        self.timezone_name = "America/Los_Angeles"
        # self.browser_platform = await self.page.evaluate("""() => { return window.navigator.platform; }""")
        self.browser_platform = "Win32"
        # self.browser_name = await self.page.evaluate("""() => { return window.navigator.appCodeName; }""")
        self.browser_name = "Mozilla"
        # self.browser_version = await self.page.evaluate("""() => { return window.navigator.appVersion; }""")
        self.browser_version = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

        self.width = "3440" #page.evaluate("""() => { return screen.width; }""")
        self.height = "1440" #page.evaluate("""() => { return screen.height; }""")

    def create_page(self, set_useragent=False):
        iphone = playwright.devices["iPhone 11 Pro"]
        iphone["viewport"] = {
            "width": random.randint(320, 1920),
            "height": random.randint(320, 1920),
        }
        iphone["deviceScaleFactor"] = random.randint(1, 3)
        iphone["isMobile"] = random.randint(1, 2) == 1
        iphone["hasTouch"] = random.randint(1, 2) == 1
        iphone['userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

        context = self.browser.newContext(**iphone)
        if set_useragent:
            self.userAgent = iphone["userAgent"]
            self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        page = context.newPage()

        return page

    def base36encode(self, number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Converts an integer to a base36 string."""
        base36 = ''
        sign = ''

        if number < 0:
            sign = '-'
            number = -number

        if 0 <= number < len(alphabet):
            return sign + alphabet[number]

        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36

        return sign + base36

    def gen_verifyFp(self):
        start_time = int(time.time() * 1000)
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[:]
        chars_len = len(chars)
        scenarioTitle = self.base36encode(int(time.time() * 1000))
        uuid = [0] * 36
        uuid[8] = '_'
        uuid[13] = '_'
        uuid[18] = '_'
        uuid[23] = '_'
        uuid[14] = "4"
        r = None
        for i in range(36):
            if uuid[i] == 0:
                if r == None:
                    r = 0
                else:
                    r = random.random() * chars_len
                uuid[i] = chars[int(r)]
        ending = ""
        for x in uuid:
            ending += str(x)
        return "verify_" + scenarioTitle + "_" + ending
    def sign_url(self, **kwargs):
        url = kwargs.get("url", None)
        if url == None:
            raise Exception("sign_url required a url parameter")
        page = self.create_page()
        verifyFp = "".join(
            random.choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            )
            for i in range(16)
        )

        if kwargs.get("gen_new_verifyFp", False):
            verifyFp = self.gen_verifyFp()
        else:
            verifyFp = kwargs.get("custom_verifyFp", "verify_khgp4f49_V12d4mRX_MdCO_4Wzt_Ar0k_z4RCQC9pUDpX")


        if kwargs.get("custom_did", None) != None:
            did = kwargs.get("custom_did", None)
        elif self.did == None:
            did = str(random.randint(10000, 999999999))
        else:
            did = self.did
        print('==== did and vfp ====')
        print(did)
        print(verifyFp)
        page.setContent("<script> " + get_acrawler() + " </script>")
        url_ben = 'https://m.tiktok.com/api/item_list/?aid=1988&app_name=tiktok_web&device_platform=web&referer=&user_agent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&cookie_enabled=true&screen_width=3440&screen_height=1440&browser_language=en-US&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&browser_online=true&ac=4g&timezone_name=America%2FLos_Angeles&page_referer=https:%2F%2Fwww.tiktok.com%2F@benthamite&priority_region=&verifyFp=verify_khgyofu6_YP8cEg4o_QpRA_4lbj_89kv_LOaIzzExQcAs&appId=1233&region=US&appType=m&isAndroid=false&isMobile=false&isIOS=false&OS=windows&did=6894770323305154053&count=30&id=6745191554350760966&secUid=MS4wLjABAAAAM3R2BtjzVT-uAtstkl2iugMzC6AtnpkojJbjiOdDDrdsTiTR75-8lyWJCY5VvDrZ&maxCursor=0&minCursor=0&sourceType=8&language=en'
        # page.goto('https://www.tiktok.com/@fallontonight')
        ben_signature = page.evaluate(
                '''() => {
        var url = "'''
                + url_ben
                + """"
        var token = window.byted_acrawler.sign({url: url});
        return token;
        }""")
        print(f'Ben signature: {ben_signature}')
        print(f'Ben URL: {url_ben}&_signature={ben_signature}')
        return (
            verifyFp,
            did,
            page.evaluate(
                '''() => {
        var url = "'''
                + url
                + "&verifyFp="
                + verifyFp
                + """&did="""
                + did
                + """"
        var token = window.byted_acrawler.sign({url: url});
        return token;
        }"""
            ),
        )
        page.close() # _02B4Z6wo00f013oBR3wAAICDcPD.EPIIsBN6MEPAAIE3b2

    def clean_up(self):
        try:
            self.browser.close()
        except:
            logging.info("cleanup failed")
        # playwright.stop()

    def find_redirect(self, url):
        self.page.goto(url, {"waitUntil": "load"})
        self.redirect_url = self.page.url

    def __format_proxy(self, proxy):
        if proxy != None:
            return {"http": proxy, "https": proxy}
        else:
            return None

    def __get_js(self):
        return requests.get(
            "https://sf16-muse-va.ibytedtos.com/obj/rc-web-sdk-gcs/acrawler.js",
            proxies=self.__format_proxy(self.proxy),
        ).text
