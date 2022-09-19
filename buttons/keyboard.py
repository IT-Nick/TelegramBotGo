from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button1 = KeyboardButton('/Включить_рассылку')
button2 = KeyboardButton('/Изменить_параметры')

keyboard = ReplyKeyboardMarkup()

keyboard.add(button1).add(button2)

change_button1 = KeyboardButton('/Период_отправки')
change_button2 = KeyboardButton('/Триггеры')
change_button3 = KeyboardButton('/Изменить_FAQ')
change_button4 = KeyboardButton('/Обратно')

change_keyboard = ReplyKeyboardMarkup()
change_keyboard.add(change_button1).add(change_button2).add(change_button3).add(change_button4)
