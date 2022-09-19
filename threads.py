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


async def send_message(user_id: int, output_text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, output_text, disable_notification=disable_notification,
                               parse_mode=ParseMode.MARKDOWN, reply_markup=inline_kb1)
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


async def broadcaster(text) -> int:
    count = 0
    try:
        for user_id in get_users():
            if await send_message(user_id, text):
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
            result += ("🟰" + key + ": `" + str(value) + "` \n")
        result += "🏷 _(RUB)_\n\n🔘 *Драг. Металлы:* ️\n"
        for key, value in zip(met, met.values()):
            result += ("🟰" + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USD/Тройская унция)_\n\n🔘 *Материалы:*️ \n"
        for key, value in zip(mat, mat.values()):
            result += ("🟰" + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USc/Фунт)_\n"
        await broadcaster(result)
        # ----------------------------

        print("broadcast сработал")


async def check_triggers(sleep_for, trigger):
    while True:
        await asyncio.sleep(sleep_for)
        # -------------FINANZ--------------
        error_cur = trigger.trgger_currency()
        for err in error_cur:
            if err:
                await broadcaster(err)
        error_met = trigger.trgger_metals()
        for err in error_met:
            if err:
                await broadcaster(err)
        error_mat = trigger.trgger_materials()
        for err in error_mat:
            if err:
                await broadcaster(err)
        localDB.trigger_price = trigger.get_current_price()
        # ----------------------------

        print("check_triggers сработал")
