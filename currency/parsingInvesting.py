from bs4 import BeautifulSoup as bs
import requests


class ParsingInvesting:
    BASE_URL = 'https://ru.investing.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

    CURRENCY_CODES = {
        'USD': "pid-2186-bid", #rub
        'EUR': "pid-1691-bid", #rub
        'GBR': "pid-2-bid", #USD
        'AUD': "pid-5-bid" #USD
    }

    METALS_CODES = {
        'Золото': "pid-8830-last",
        'Палладий': "pid-8883-last",
        'Платина': "pid-8910-last",
        'Серебро': "pid-8836-last"
    }

    MATERIALS_CODES = {
        'Хлопок': "pid-8851-last"
    }

    def get_currency_price(self):
        results_curr = {}
        extra_url = 'currencies/streaming-forex-rates-majors'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for currency_code in self.CURRENCY_CODES.keys():
            element_curr = soup.find("td", {"class": self.CURRENCY_CODES.get(currency_code)})
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(currency_code + ": " + total_price)
            results_curr[currency_code] = total_price
        return results_curr

    def get_metals_price(self):
        results_met = {}
        extra_url = 'commodities/metals'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for metal_code in self.METALS_CODES.keys():
            element_curr = soup.find("td", {"class": self.METALS_CODES.get(metal_code)})
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(metal_code + ": " + total_price)
            results_met[metal_code] = total_price
        return results_met

    def get_materials_price(self):
        results_mat = {}
        extra_url = 'birzhevyye-tovary/v-realnom-vremeni'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for metal_code in self.MATERIALS_CODES.keys():
            element_curr = soup.find("td", {"class": self.MATERIALS_CODES.get(metal_code)})
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(metal_code + ": " + total_price)
            results_mat[metal_code] = total_price
        return results_mat
