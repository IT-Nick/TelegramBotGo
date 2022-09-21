import logging
import os
from aiogram.utils import executor
from create import dp, TOKEN, bot
from handlers import client
from threads import check_triggers, broadcast, broadcastInvesting, broadcastTrade
from aiogram import asyncio
from triggers.triggerFinanz import TriggerFinanz
from triggers.triggerInvesting import TriggerInvesting
from triggers.triggerTrading import TriggerTrading
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
   interval_broadcast = 20
   interval_triggers = 10
   interval_Trade = 4
   interval_investing = 30
   trigger = TriggerFinanz()
   trigger.set_current_price()
   triggerInv = TriggerInvesting()
   triggerInv.set_current_price()
   triggerTrd = TriggerTrading()
   triggerTrd.set_current_price()
   client.register_handlers(dp)
   loop = asyncio.get_event_loop()
   loop.create_task(broadcast(interval_broadcast, trigger))
   loop.create_task(broadcastInvesting(interval_investing, triggerInv))
   loop.create_task(broadcastTrade(interval_Trade, triggerTrd))
   loop.create_task(check_triggers(interval_triggers, trigger, triggerInv))
   await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()    


    
   

#executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
   logging.basicConfig(level=logging.INFO)
   start_webhook(
       dispatcher=dp,
       webhook_path=WEBHOOK_PATH,
       skip_updates=True,
       on_startup=on_startup,
       on_shutdown=on_shutdown,
       host=WEBAPP_HOST,
       port=WEBAPP_PORT,
   )
