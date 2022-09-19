import logging
import os
from aiogram.utils import executor
from create import dp, TOKEN
from handlers import client
from threads import check_triggers, broadcast
from aiogram import asyncio
from triggers.triggerFinanz import TriggerFinanz
from aiogram.utils.executor import start_webhook


HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

async def on_startup(dispatcher):
    print("sd")



    
    
interval_broadcast = 20
interval_triggers = 10

trigger = TriggerFinanz()
trigger.set_current_price()

client.register_handlers(dp)

loop = asyncio.get_event_loop()
loop.create_task(broadcast(interval_broadcast, trigger))
loop.create_task(check_triggers(interval_triggers, trigger))

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



