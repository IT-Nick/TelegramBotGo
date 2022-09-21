import asyncio
from create import bot
from aiogram.utils import exceptions
from database import localDB
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


def get_users():
    """
    Возвращает список пользователей
    из локальной базы данных
    """
    yield from localDB.database


inline_btn_1 = InlineKeyboardButton('finanz.ru', url='https://www.finanz.ru/birzhevyye-tovary/v-realnom-vremeni')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_2 = InlineKeyboardButton('investing.com', url='https://ru.investing.com/commodities/metals')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2)

inline_btn_3 = InlineKeyboardButton('tradingeconomics.com', url='https://tradingeconomics.com/russia/forecast')
inline_kb3 = InlineKeyboardMarkup().add(inline_btn_3)

async def send_message(user_id: int, output_text: str, hint: str, disable_notification: bool = False) -> bool:
    try:
        if hint == "finanz":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "investing":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "hint":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN)
        elif hint == "trading":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb3)
        elif hint == "triggerFinMat":
            await bot.send_message(user_id,output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "triggerInvCur":
            await bot.send_message(user_id, ("⚠️Сработал триггер! \n" + output_text+ "\n #triggerInvestingCurrency"), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "triggerInvMet":
            await bot.send_message(user_id, ("⚠️Сработал триггер! \n" + output_text+ "\n #triggerInvestingMetal"), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "triggerInvMat":
            await bot.send_message(user_id, ("⚠️Сработал триггер! \n" + output_text + "\n #triggerInvestingMaterial"), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
    except exceptions.BotBlocked:
        print(f"Отправка [ID:{user_id}]: заблокирована пользователем")
    except exceptions.ChatNotFound:
        print(f"Отправка [ID:{user_id}]: id не найден")
    except exceptions.RetryAfter as e:
        print(f"Отправка [ID:{user_id}]: достигнуто ограничение на отправку сообщений. Ожидание {e.timeout} секунд")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, output_text)  # Пробуем еще раз
    except exceptions.UserDeactivated:
        print(f"Отправка [ID:{user_id}]: пользователь не активен")
    except exceptions.TelegramAPIError:
        print(f"Отправка [ID:{user_id}]: ошибка")
    else:
        print(f"Отправка [ID:{user_id}]: успешно")
        return True
    return False


async def broadcaster(text, hint) -> int:
    count = 0
    try:
        for user_id in get_users():
            if await send_message(user_id, text, hint):
                count += 1
            await asyncio.sleep(.05)  # 20 сообщений в секунду (Ограничение телеграмм: 30 сообщений в секунду)
    finally:
        print(f"{count} сообщение успешно доставлено.")

    return count  # кол-во отправленных сообщений

def merge(dict, hints):
    if hints == "finanz":
        localDB.triggerFull_price_finanz = {**localDB.triggerFull_price_finanz, **dict}
    if hints == "investing":
        localDB.triggerFull_price_investing = {**localDB.triggerFull_price_investing, **dict}
    if hints == "trading":
        localDB.triggerFull_price_trading = {**localDB.triggerFull_price_trading, **dict}
    return res

async def broadcast(sleep_for, trigger):
    counter = 0
    while True:
        await asyncio.sleep(sleep_for)
        # -------------FINANZ--------------
        curr = trigger.finanz.get_currency_price()
        met = trigger.finanz.get_metals_price()
        mat = trigger.finanz.get_materials_price()
        merge(curr, "finanz")
        merge(met, "finanz")
        merge(mat, "finanz")
        z = {**dis, **dic} 
        print("ТРИГГЕРНАЯ ЦЕНА")
        print(trigger.get_current_price())
        if counter < 4:
            result = '*Биржевая информация*                           🧷\n\n🔘 *Валюта:*\n'
            for key, value in zip(curr, curr.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "🏷 _(RUB)_\n\n🔘 *Драг. Металлы:* ️\n"
            for key, value in zip(met, met.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "🏷 _(USD/Тройская унция)_\n\n🔘 *Материалы:*️ \n"
            for key, value in zip(mat, mat.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "🏷 _(USc/Фунт)_\n"
            await broadcaster(result, "finanz")
            counter += 1
        else:
            await broadcaster(localDB.triggerFull_price_finanz, "finanz")
            localDB.triggerFull_price_finanz.update({})
            counter = 0
            
        # ----------------------------

        print("broadcast сработал")

        
async def broadcastInvesting(sleep_for, trigger):
    counter = 0
    while True:
        await asyncio.sleep(sleep_for)
        # -------------INVESTING--------------
        curr = trigger.finanz.get_currency_price()
        met = trigger.finanz.get_metals_price()
        mat = trigger.finanz.get_materials_price()
        merge(curr, "investing")
        merge(met, "investing")
        merge(mat, "investing")
        print("ТРИГГЕРНАЯ ЦЕНА")
        print(trigger.get_current_price())
        if counter < 4:
            result = '*Биржевая информация*                           🧷\n\n🔘 *Валюта:*\n'
            i = 0
            slash = ['RUB', 'RUB', 'USD', 'USD']
            for key, value in zip(curr, curr.values()):
                result += (" " + key + "/" + slash[i] + ": `" + str(value) + "` \n")
                i += 1
            result += "\n\n🔘 *Драг. Металлы:* ️\n"
            for key, value in zip(met, met.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "\n\n🔘 *Материалы:*️ \n"
            for key, value in zip(mat, mat.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "\n"
            await broadcaster(result, "investing")
            counter += 1
        else:
            await broadcaster(localDB.triggerFull_price_investing, "investing")
            localDB.triggerFull_price_investing.update({})
            counter = 0
        # ----------------------------

        print("broadcast сработал")

async def broadcastTrade(sleep_for, trigger):
    counter = 0
    while True:
        await asyncio.sleep(sleep_for)
        # -------------INVESTING--------------
        curr = trigger.finanz.get_currency_price()
        met = trigger.finanz.get_metals_price()
        mat = trigger.finanz.get_materials_price()
        merge(curr, "trading")
        merge(met, "trading")
        merge(mat, "trading")
        print("ТРИГГЕРНАЯ ЦЕНА")
        print(trigger.get_current_price())
        if counter < 4:
            result = '*Биржевая информация*                           🧷\n\n🔘 *Валюта:*\n'
            i = 0
            slash = ['RUB', 'RUB', 'USD', 'USD']
            for key, value in zip(curr, curr.values()):
                result += (" " + key + "/" + slash[i] + ": `" + str(value) + "` \n")
                i += 1
            result += "\n\n🔘 *Драг. Металлы:* ️\n"
            for key, value in zip(met, met.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "\n\n🔘 *Материалы:*️ \n"
            for key, value in zip(mat, mat.values()):
                result += (" " + key + ": `" + str(value) + "` \n")
            result += "\n"
            await broadcaster(result, "investing")
        else:
            await broadcaster(localDB.triggerFull_price_trading, "trading")
            localDB.triggerFull_price_trading.update({})
            counter = 0
        # ----------------------------

        print("broadcast сработал")
        
async def check_triggers(sleep_for, trigger, triggerInv):
    while True:
        await asyncio.sleep(sleep_for)
        await broadcaster("*Подсказка*: если индекс падает – можно просить скидку, если растет – быть готовым к сдерживать рост цен. ", "hint")
        # -------------FINANZ--------------
        localDB.trigger_price = trigger.get_current_price()
        # -------------Investing--------------
        localDB.triggerInv_price = triggerInv.get_current_price()
        # ----------------------------

        print("check_triggers сработал")
