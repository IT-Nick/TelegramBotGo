
from bs4 import BeautifulSoup as bs
import requests

print("\033[34m ssd\033[0m")
CURRENCY_CODES = {
    'USD': "Y0101095000839420",
    'EUR': "Y0101095000946869",
    'GBR': "Y0101095000839173",
    'JPY': "Y0101095000851534",
    'AUD': "Y0101095000851636"}
for currency_code in CURRENCY_CODES.keys():
    print(currency_code, CURRENCY_CODES.get(currency_code))

base_url = 'https://www.finanz.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

def currency():
    extra_url = 'valyuty/v-realnom-vremeni-rub'
    full_page = requests.get(base_url + extra_url, headers=headers)
    soup = bs(full_page.content, "html.parser")
    USD = soup.find("div", {"data-item": "Y0101095000839420"}).find("span")
    print('USD: ' + USD.text)
    EUR = soup.find("div", {"data-item": "Y0101095000946869"}).find("span")
    print('EUR: ' + EUR.text)
    GBP = soup.find("div", {"data-item": "Y0101095000839173"}).find("span")
    print('GBP: ' + GBP.text)
    JPY = soup.find("div", {"data-item": "Y0101095000851534"}).find("span")
    print('JPY: ' + JPY.text)
    AUD = soup.find("div", {"data-item": "Y0101095000851636"}).find("span")
    print('AUD: ' + AUD.text)

def metals():
    extra_url = 'birzhevyye-tovary/v-realnom-vremeni'
    full_page = requests.get(base_url + extra_url, headers=headers)

    soup = bs(full_page.content, "html.parser")
    GOLD = soup.find("div", {"data-item": "Y0306000000XAU"}).find("span")
    res = GOLD.text.replace("Т", "").replace(" ", "").replace(",", ".")
    print('GOLD: ' + res)
    PAL = soup.find("div", {"data-item": "Y0306000000XPD"}).find("span")
    print('PAL: ' + PAL.text.replace("Т", "").replace(" ", "").replace(",", "."))
    PLA = soup.find("div", {"data-item": "Y0306000000XPT"}).find("span")
    print('PLA: ' + PLA.text.replace("Т", "").replace(" ", "").replace(",", "."))
    SIL = soup.find("div", {"data-item": "Y0306000000XAG"}).find("span")
    print('SIL: ' + SIL.text.replace("Т", "").replace(" ", "").replace(",", "."))

def materials():
    extra_url = 'birzhevyye-tovary/v-realnom-vremeni'
    full_page = requests.get(base_url + extra_url, headers=headers)

    soup = bs(full_page.content, "html.parser")
    GOLD = soup.find("div", {"data-item": "Y0306000000XAU"}).find("span")
    res = GOLD.text.replace("Т", "").replace(" ", "").replace(",", ".")
    print('GOLD: ' + res)
    PAL = soup.find("div", {"data-item": "Y0306000000XPD"}).find("span")
    print('PAL: ' + PAL.text.replace("Т", "").replace(" ", "").replace(",", "."))
    PLA = soup.find("div", {"data-item": "Y0306000000XPT"}).find("span")
    print('PLA: ' + PLA.text.replace("Т", "").replace(" ", "").replace(",", "."))
    SIL = soup.find("div", {"data-item": "Y0306000000XAG"}).find("span")
    print('SIL: ' + SIL.text.replace("Т", "").replace(" ", "").replace(",", "."))


print("Валюта")
currency()
print("Металд & Материал")
metals()

#from triggers.triggerMOEX import Trigger
#import asyncio
#import datetime
#import random
#
#
#async def my_sleep_func():
#    await asyncio.sleep(random.randint(0, 5))
#
#
#async def display_date(num, loop, t):
#    end_time = loop.time() + 50.0
#    while True:
#        t.trgger_currency_moex()
#
#        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
#        if (loop.time() + 1.0) >= end_time:
#            break
#        await my_sleep_func()
#
#
#loop = asyncio.get_event_loop()
#
#t = Trigger()
#t.set_current_moex_price()
#
#asyncio.ensure_future(display_date(1, loop, t))
#asyncio.ensure_future(display_date(2, loop, t))
#
#loop.run_forever()
#
#