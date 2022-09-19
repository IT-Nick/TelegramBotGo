from bs4 import BeautifulSoup as bs
import requests


class ParsingFinanz:
    BASE_URL = 'https://www.finanz.ru/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

    CURRENCY_CODES = {
        'USD': "Y0101095000839420",
        'EUR': "Y0101095000946869",
        'GBR': "Y0101095000839173",
        'JPY': "Y0101095000851534",
        'AUD': "Y0101095000851636"
    }

    METALS_CODES = {
        'Золото': "Y0306000000XAU",
        'Палладий': "Y0306000000XPD",
        'Платина': "Y0306000000XPT",
        'Серебро': "Y0306000000XAG"
    }

    MATERIALS_CODES = {
        'Хлопок': "Y0306000000"
    }

    def get_currency_price(self):
        results_curr = {}
        extra_url = 'valyuty/v-realnom-vremeni-rub'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for currency_code in self.CURRENCY_CODES.keys():
            element_curr = soup.find("div", {"data-item": self.CURRENCY_CODES.get(currency_code)}).find("span")
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(currency_code + ": " + total_price)
            results_curr[currency_code] = total_price
            #RUB
        return results_curr

    def get_metals_price(self):
        results_met = {}
        extra_url = 'birzhevyye-tovary/v-realnom-vremeni'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for metal_code in self.METALS_CODES.keys():
            element_curr = soup.find("div", {"data-item": self.METALS_CODES.get(metal_code)}).find("span")
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(metal_code + ": " + total_price)
            results_met[metal_code] = total_price
            #USD/Тройская унция
        return results_met

    def get_materials_price(self):
        results_mat = {}
        extra_url = 'birzhevyye-tovary/v-realnom-vremeni'
        full_page = requests.get(self.BASE_URL + extra_url, headers=self.headers)
        soup = bs(full_page.content, "html.parser")
        for metal_code in self.MATERIALS_CODES.keys():
            element_curr = soup.find_all("div", {"data-item": self.MATERIALS_CODES.get(metal_code)})[12].find("span")
            total_price = element_curr.text.replace("Т", "").replace(" ", "").replace(",", ".")
            print(metal_code + ": " + total_price)
            results_mat[metal_code] = total_price
            #USc/Фунт
        return results_mat
