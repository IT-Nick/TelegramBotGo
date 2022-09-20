from aiogram import types, Dispatcher
from aiogram.types import ParseMode
from currency.parsingFinanz import ParsingFinanz

from create import bot
from database import localDB


keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


async def command_start(message: types.Message):
    more_btns_text = (
        "📉 Текущая цена",
        "📈 Триггерная цена"
    )
    keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))

    await message.reply("Привет! 👋\nТы был подключен к общей рассылке биржевой информации! \n\nТы можешь в любое время узнать текущую стоимость, не дожидаясь следующей рассылки! Для этого нажми на кнопку \n📉 Текущая цена\n\nЧтобы узнать, от какой суммы отталкивается триггер, жми \n📈 Триггерная цена \n\nЕсли клавиатура пропала, пиши восклицательный знак !", reply_markup=keyboard_markup)
    localDB.database.append(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Твой ID: ' + str(message.from_user.id))


keyboard_markup_params = types.ReplyKeyboardMarkup(resize_keyboard=True)


async def start_messaging(message: types.Message):
    button_text = message.text

    if button_text == '📉 Текущая цена':
        parser_finanz = ParsingFinanz()
        curr = parser_finanz.get_currency_price()
        met = parser_finanz.get_metals_price()
        mat = parser_finanz.get_materials_price()
        result = '*Цены на данный момент*                        🧷\n\n🔘 *Валюта:*\n'
        for key, value in zip(curr, curr.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(RUB)_\n\n🔘 *Драг. Металлы:* ️\n"
        for key, value in zip(met, met.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USD/Тройская унция)_\n\n🔘 *Материалы:*️ \n"
        for key, value in zip(mat, mat.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USc/Фунт)_\n"
        await message.reply(result, reply_markup=keyboard_markup, parse_mode=ParseMode.MARKDOWN)
    elif button_text == '📈 Триггерная цена':
        price = localDB.trigger_price
        priceInv = localDB.triggerInv_price
        print("Триггерная цена")
        print(price)
        print(priceInv)
        result = '*Стартовая цена*\n\nFINANZ\n'
        for key, value in zip(price, price.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "INVESTING\n"
         for key, value in zip(priceInv, priceInv.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += '\nПри повышении или понижении этих цен на указанные проценты, сработает триггер!'
        await message.reply(result, reply_markup=keyboard_markup, parse_mode=ParseMode.MARKDOWN)
    elif button_text == '!':
        await message.reply("Открываю клавиатуру...", reply_markup=keyboard_markup)




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'Обратно'])
    dp.register_message_handler(start_messaging)
