from bs4 import BeautifulSoup as bs
import requests


class ParsingMOEX:
    CURRENCY_CODES = ['USD_RUB', 'EUR_RUB', 'JPY_RUB', 'GBP_RUB']  # AUD_RUB не найдено на moex
    METALS_CODES = []
    MATERIALS_CODES = []

    def get_currency_price(self):
        results_cur = {}
        for currency_code in self.CURRENCY_CODES:
            url_template = "https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=" + currency_code
            full_page = requests.get(url_template)
            soup = bs(full_page.content, "html.parser")
            convert = soup.find("span", {"id": "ctl00_PageContent_tbxCurrentRate"}).find('b')
            total_price = convert.text.replace(",", ".").replace("Текущее значение:  ", "")
            results_cur.update({currency_code: total_price})
        return results_cur

    def get_metals_price(self):
        results_met = {}
        for metal_code in self.METALS_CODES:
            url_template = "https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=" + metal_code
            full_page = requests.get(url_template)
            soup = bs(full_page.content, "html.parser")
            convert = soup.find("span", {"id": "ctl00_PageContent_tbxCurrentRate"}).find('b')
            total_price = convert.text.replace(",", ".").replace("Текущее значение:  ", "")
            results_met.update({metal_code: total_price})
        return results_met

    def get_materials_price(self):
        results_mat = {}
        for material_code in self.MATERIALS_CODES:
            url_template = "https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=" + material_code
            full_page = requests.get(url_template)
            soup = bs(full_page.content, "html.parser")
            convert = soup.find("span", {"id": "ctl00_PageContent_tbxCurrentRate"}).find('b')
            total_price = convert.text.replace(",", ".").replace("Текущее значение:  ", "")
            results_mat.update({material_code: total_price})
        return results_mat
