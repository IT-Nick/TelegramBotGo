from bs4 import BeautifulSoup as bs
import requests


class ParsingSPB:
    CURRENCY_CODES = ['USD_RUB', 'EUR_RUB', 'JPY_RUB', 'GBP_RUB']  # AUD_RUB не найдено на moex

    def parse_currency(currency_code):
        url_template = "https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=" + currency_code
        return url_template

    def get_currency_price(self):
        results = {}
        for currency_code in self.CURRENCY_CODES:
            url_template = "https://www.moex.com/ru/derivatives/currency-rate.aspx?currency=" + currency_code
            full_page = requests.get(url_template)
            soup = bs(full_page.content, "html.parser")
            convert = soup.find("span", {"id": "ctl00_PageContent_tbxCurrentRate"}).find('b')
            total_price = convert.text.replace(",", ".").replace("Текущее значение:  ", "")
            results.update({currency_code: total_price})
        return results

#
# TIKER = 'OZON'
# ID = 0
# CUR = ""
# class Parsing:
#    TIKER = 'OZON'
#    URL_TEMPLATE = ""
#    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
#
#    current_convertated_price = 0
#    difference = 5
#
#    def first_init(self):
#        self.URL_TEMPLATE =  "https://www.tinkoff.ru/invest/stocks/" + TIKER + "/"
#        self.current_convertated_price = float(self.get_currency_price())
#
#
#    def get_currency_price(self):
#        full_page = requests.get(self.URL_TEMPLATE)
#
#        soup = bs(full_page.content, "html.parser")
#
#        convert = soup.find("span", {"class": "Money-module__money_UZBbh"})
#        return convert.text.replace(",", ".").replace("\xa0", "").replace("₽", "").replace(" ", "")
#
#
#    def check_currency(self):
#        currency = float(self.get_currency_price())
#        if currency >= self.current_convertated_price + self.difference:
#            print("Курс тикера " + TIKER + " вырос на 5 рублей!")
#        elif currency <= self.current_convertated_price - self.difference:
#            print("Курс тикера " + TIKER + " упал на 5 рублей!")
#        global CUR 
#        CUR = str(currency)
#        print("Курс тикера " + TIKER + " = " + CUR)
#        #time.sleep(3)
#        #self.check_currency()
#
#
