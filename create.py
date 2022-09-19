from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)
