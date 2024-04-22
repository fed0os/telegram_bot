import telebot
from telebot import TeleBot
from app.db.db_connect import connect_to_db
from employee_functions import show_employees_table, show_all_employee, show_employees_salary
from foundry_functions import show_foundry_table, show_no_processed_details
from storage_functions import show_storage_table, show_our_storage, show_dima_storage

bot = TeleBot('6601289362:AAHP8IfBXJ4vczvZKBFvDBBDT752UbwGW0k')
name = ''


@bot.message_handler(commands=['start'])
def greeting_table(message):
    bot.send_message(message.chat.id, "Приветствую в нашем боте")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Литье', callback_data='casting'))
    markup.add(telebot.types.InlineKeyboardButton('Метал', callback_data='aluminium'))
    markup.add(telebot.types.InlineKeyboardButton('Склад', callback_data='storage'))
    markup.add(telebot.types.InlineKeyboardButton('Покупатели', callback_data='customers'))
    markup.add(telebot.types.InlineKeyboardButton('Сотрудники', callback_data='employees'))
    bot.send_message(message.chat.id, 'Выберите пунтк', reply_markup=markup)


@connect_to_db
def my_callback(conn, cursor, call):
    if call.data == 'employees':
        show_employees_table(bot, call)
    elif call.data == 'employees list':
        show_all_employee(bot, call, cursor)
    elif call.data == 'salary':
        show_employees_salary(bot, call, cursor)
    elif call.data == 'products produced':
        bot.send_message(call.message.chat.id, 'Кто сколько положил на склад или отлил')

    if call.data == 'aluminium': ...

    if call.data == 'casting':
        show_foundry_table(bot, call)
    elif call.data == 'No details processed':
        show_no_processed_details(bot, call, cursor)
    elif call.data == 'Add details':
        bot.send_message(call.message.chat.id, 'Позже будет возможность добавить детали')

    if call.data == 'storage':
        show_storage_table(bot, call)
    elif call.data == 'our storage':
        show_our_storage(bot, call, cursor)
    elif call.data == 'dima storage':
        show_dima_storage(bot, call, cursor)


@bot.callback_query_handler(func=lambda call: True)
def callback_wrapper(call):
    my_callback(call)


bot.polling(non_stop=True)
