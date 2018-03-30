from models.heuristic import Heuristic
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from boilerpipe.extract import Extractor
from multiprocessing import RLock
from bs4 import BeautifulSoup, SoupStrainer
import re

# Procedural 2q
# Ensure link to EULA can be found on home page
class DirectPresentation(Heuristic):
    def score(self, eula):
        if eula.url is None:
            return {'score': -1, 'max': 4, 'reason': 'no url'}
        else:
            url = eula.url
            suffixes = [".com", ".net", ".org"]
            for i in suffixes:
                n = url.find(i)
                if n != -1:
                    break
            url = url[0:n+4]

            chrome_options = Options()
            chrome_options.add_argument("--hide-scrollbars")
            chrome_options.set_headless()

            # Start chrome driver, and set window to initial width and height
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_window_size(1920, 1080)

            # Grab desktop view
            driver.get(url)
            html = driver.page_source

            pattern = re.compile(r'terms')
            soup = BeautifulSoup(html, 'html.parser')
            search = soup.findAll('a', href=True, text=re.compile(r'end\W*user\W*license', re.I))
            if len(search) == 1:
                return {'score': 4, 'max': 4, 'eula_found': search[0]['href']}
            elif len(search) > 1:
                return {'score': 4, 'max': 4, 'possible_eulas': search}

            search = soup.findAll('a', href=True, text=re.compile(r'terms', re.I))
            if len(search) == 1:
                return {'score': 4, 'max': 4, 'eula_found': search[0]['href']}
            elif len(search) > 1:
                return {'score': 4, 'max': 4, 'possible_eulas': search}

        return {'score': 0, 'max': 4, 'reason': 'Could not find link to EULA on homepage'}
