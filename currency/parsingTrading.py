from bs4 import BeautifulSoup as bs
import requests


class ParsingTrading:
    BASE_URL = 'https://tradingeconomics.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

    CURRENCY_CODES = {
        'USDRUB': 0,
        'EURRUB': 1,
        'GBPRUB': 2,
        'AUDRUB': 3,
        'RUBJPY': 5
    }

    CORE_CODES = {
        'Core Inflation Rate': 20,
        'Food Inflation': 40
    }

    FOOD_CODES = {
        'Хлопок': "pid-8851-last"
    }

    GASOLINE_CODES = {
        'Хлопок': "pid-8851-last"
    }
    def get_currency_price(self):
        results_curr = {}
        extra_url = 'russia/currency'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for currency_code in self.CURRENCY_CODES.keys():
            element_curr = soup.find_all("table", {"class": "table table-hover sortable-theme-minimal table-heatmap"})[1].find_all("td", {"id": "p"})[self.CURRENCY_CODES.get(currency_code)]
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(currency_code + ": " + total_price)
            results_curr[currency_code] = total_price
        return results_curr

    def get_metals_price(self):
        results_curr = {}
        extra_url = 'russia/core-inflation-rate'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for currency_code in self.CORE_CODES.keys():
            element_curr = soup.find_all("table", {"class": "table table-hover"})[0].find_all("td")[self.CORE_CODES.get(currency_code)]
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(currency_code + ": " + total_price)
            results_curr[currency_code] = total_price
        return results_curr

    def get_materials_price(self):
        results_curr = {}
        extra_url = 'russia/currency'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for currency_code in self.CURRENCY_CODES.keys():
            element_curr = soup.find_all("table", {"class": "table table-hover sortable-theme-minimal table-heatmap"})[1].find_all("td", {"id": "p"})[self.CURRENCY_CODES.get(currency_code)]
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(currency_code + ": " + total_price)
            results_curr[currency_code] = total_price
        return results_curr
