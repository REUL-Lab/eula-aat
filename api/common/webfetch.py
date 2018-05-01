""" Handles the fetching of requests on the web.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from boilerpipe.extract import Extractor
from multiprocessing import RLock

import requests
# Specify a specific build using the following two arguments
#"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    #"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }


class FetchService:
    def __init__(self, url, desk_width=1920, desk_height=1080, mobile_width=360, mobile_height=640, mobile_pixel_ratio=3.0):
        self.url = url

        # Make sure status code is 200
        r = requests.head(url)

        # Attempt to follow redirects
        attempts = 0
        while r.status_code == 301 and attempts < 3:
            # If no location to follow through, give up
            if 'Location' not in r.headers:
                raise requests.ConnectionError
            # Navigate to new location
            r = requests.head(r.headers['Location'])
            attempts = attempts + 1

        if r.status_code != 200:
            # Throw exception with status code
            raise requests.ConnectionError(str(r.status_code))

        chrome_options = Options()  
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.set_headless()

        # Start chrome driver, and set window to initial width and height
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(desk_width, desk_height)

        # Grab desktop view
        driver.get(self.url)

        # Expand height to be the full length of the page for image processing
        height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        driver.set_window_size(desk_width, height + 100)

        # Extract text from desktop view
        self.__html = driver.page_source
        extractor = Extractor(extractor='ArticleExtractor', html=self.__html)
        self.__text = extractor.getText()

        # Add a lock to the driver so there are no access colisions during threaded execution
        driver.lock = RLock()
        
        # We need to save this driver in order for heuristics to analyse the DOM
        self.__desk_driver = driver

        # Start chrome for mobile view
        mobile_emulation = {"deviceMetrics": { "width": mobile_width, "height": mobile_height, "pixelRatio": mobile_pixel_ratio },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

        # Enable mobile emulation for headless
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # Nav to page and expand to full view
        driver.get(self.url)
        height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        
        # Add a lock to the driver so there are no access colisions during threaded execution
        driver.lock = RLock()

        # We need to save this driver in order for heuristics to analyse the mobile DOM
        self.__mobile_driver = driver

    def extract_text(self):
        return self.__text

    def get_desk_driver(self):
        return self.__desk_driver

    def get_mobile_driver(self):
        return self.__mobile_driver

    def get_html(self):
        return self.__html
