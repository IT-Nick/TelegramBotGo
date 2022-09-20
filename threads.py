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

async def send_message(user_id: int, output_text: str, hint: str, disable_notification: bool = False) -> bool:
    try:
        if hint == "finanz":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "investing":
            await bot.send_message(user_id, output_text, disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "triggerFinCur":
            await bot.send_message(user_id, ("triggerFinCur: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "triggerFinMet":
            await bot.send_message(user_id, ("triggerFinMet: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "triggerFinMat":
            await bot.send_message(user_id, ("triggerFinMat: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
        elif hint == "triggerInvCur":
            await bot.send_message(user_id, ("triggerInvCur: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "triggerInvMet":
            await bot.send_message(user_id, ("triggerInvMet: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
        elif hint == "triggerInvMat":
            await bot.send_message(user_id, ("triggerInvMat: " + output_text), disable_notification=disable_notification, parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb2)
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


async def broadcast(sleep_for, trigger):
    while True:
        await asyncio.sleep(sleep_for)
        # -------------FINANZ--------------
        curr = trigger.finanz.get_currency_price()
        met = trigger.finanz.get_metals_price()
        mat = trigger.finanz.get_materials_price()
        print("ТРИГГЕРНАЯ ЦЕНА")
        print(trigger.get_current_price())
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
        # ----------------------------

        print("broadcast сработал")

        
async def broadcastInvesting(sleep_for, trigger):
    while True:
        await asyncio.sleep(sleep_for)
        # -------------INVESTING--------------
        curr = trigger.finanz.get_currency_price()
        met = trigger.finanz.get_metals_price()
        mat = trigger.finanz.get_materials_price()
        print("ТРИГГЕРНАЯ ЦЕНА")
        print(trigger.get_current_price())
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
        # ----------------------------

        print("broadcast сработал")

async def check_triggers(sleep_for, trigger, triggerInv):
    while True:
        await asyncio.sleep(sleep_for)
        # -------------FINANZ--------------
        error_cur = trigger.trgger_currency()
        for err in error_cur:
            if err:
                await broadcaster(err, "triggerFinCur")
        error_met = trigger.trgger_metals()
        for err in error_met:
            if err:
                await broadcaster(err, "triggerFinMet")
        error_mat = trigger.trgger_materials()
        for err in error_mat:
            if err:
                await broadcaster(err, "triggerFinMat")
        localDB.trigger_price = trigger.get_current_price()
        # -------------Investing--------------
        error_cur = triggerInv.trgger_currency()
        for err in error_cur:
            if err:
                await broadcaster(err, "triggerInvCur")
        error_met = triggerInv.trgger_metals()
        for err in error_met:
            if err:
                await broadcaster(err, "triggerInvMet")
        error_mat = triggerInv.trgger_materials()
        for err in error_mat:
            if err:
                await broadcaster(err, "triggerInvMat")
        localDB.triggerInv_price = triggerInv.get_current_price()
        # ----------------------------

        print("check_triggers сработал")
