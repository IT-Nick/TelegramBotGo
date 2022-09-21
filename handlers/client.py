from aiogram import types, Dispatcher
from aiogram.types import ParseMode
from currency.parsingFinanz import ParsingFinanz
from currency.parsingInvesting import ParsingInvesting
from currency.parsingTrading import ParsingTrading

from create import bot
from database import localDB


async def command_start(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add("📉 Текущая цена")

    await message.reply("Добрый день! 👋\nВы были подключены к общей рассылке отдела Закупок в России по рыночным индексам!\n\nВы можете получать актуальную информацию раз в сутки об изменениях основных факторов, влияющих на цену у поставщиков 📉", reply_markup=keyboard_markup)
    #localDB.database.append(message.from_user.id)
    if message.from_user.id not in localDB.database: localDB.database.append(message.from_user.id)


keyboard_markup_params = types.ReplyKeyboardMarkup(resize_keyboard=True)


async def start_messaging(message: types.Message):
    button_text = message.text

    if button_text == '📉 Текущая цена':
        parser_finanz = ParsingFinanz()
        parser_investing = ParsingInvesting()
        parser_trading = ParsingTrading()

        currF = parser_finanz.get_currency_price()
        metF = parser_finanz.get_metals_price()
        matF = parser_finanz.get_materials_price()
        result = '*Цены на данный момент*                        🧷\n\n*finanz.ru*\n🔘 *Валюта*\n'
        for key, value in zip(currF, currF.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(RUB)_\n🔘 *Драг. Металлы:* ️\n"
        for key, value in zip(metF, metF.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USD/Тройская унция)_\n🔘 *Материалы:*️ \n"
        for key, value in zip(matF, matF.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USc/Фунт)_\n"
        
        currI = parser_investing.get_currency_price()
        metI = parser_investing.get_metals_price()
        matI = parser_investing.get_materials_price()
        
        result += '\n🔘 *investing.com*\n🔘 *Валюта*\n'
        i = 0
        slash = ['RUB', 'RUB', 'USD', 'USD']
        for key, value in zip(currI, currI.values()):
            result += (" " + key + "/" + slash[i] + ": `" + str(value) + "` \n")
            i += 1
        result += "\n🔘 *Драг. Металлы:* ️\n"
        for key, value in zip(metI, metI.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "\n🔘 *Материалы:*️ \n"
        for key, value in zip(matI, matI.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "\n"
        
        currT = parser_trading.get_currency_price()
        metT = parser_trading.get_metals_price()
        matT = parser_trading.get_materials_price()
        
        result += '\n🔘 *tradingeconomics.com*\n🔘 *Валюта*\n'
        for key, value in zip(currT, currT.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(RUB)_\n🔘 *Драг. Металлы:* ️\n"
        for key, value in zip(metT, metT.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USD/Тройская унция)_\n🔘 *Материалы:*️ \n"
        for key, value in zip(matT, matT.values()):
            result += (" " + key + ": `" + str(value) + "` \n")
        result += "🏷 _(USc/Фунт)_\n"
        await message.reply(result, parse_mode=ParseMode.MARKDOWN)




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'Обратно'])
    dp.register_message_handler(start_messaging)
