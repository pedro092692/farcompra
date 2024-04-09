import requests
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings()

URL = 'https://www.bcv.org.ve'
class DollarScrapper:
    def __init__(self):
        self.url = URL
        self.dollar_value = self.scrap_value()

    def web_content(self):
        try:
            response = requests.get(self.url, verify=False)
            response.raise_for_status()
            if response.status_code == 200:
                return response.text
        except requests.exceptions.ConnectionError as e:
            print('Sorry Connection error')

    def scrap_value(self):
        content = self.web_content()
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.find_all(name='strong')
            dollar_value = float(content[-1].string.replace(" ", "").replace(",", "."))
            return float(format(dollar_value, '.3f'))
