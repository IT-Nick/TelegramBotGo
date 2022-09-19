from aiogram.utils import executor
from create import dp
from handlers import client
from threads import check_triggers, broadcast
from aiogram import asyncio
from triggers.triggerFinanz import TriggerFinanz



async def on_startup(_):
    print('Бот онлайн')


interval_broadcast = 20
interval_triggers = 10

trigger = TriggerFinanz()
trigger.set_current_price()

client.register_handlers(dp)

loop = asyncio.get_event_loop()
loop.create_task(broadcast(interval_broadcast, trigger))
loop.create_task(check_triggers(interval_triggers, trigger))

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
