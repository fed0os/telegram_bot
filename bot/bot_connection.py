import telebot
from telebot import TeleBot
import pyodbc
from db.db_connect import connect_to_db
from employee_functions import show_employees_table, show_all_employee

bot = TeleBot('6601289362:AAHP8IfBXJ4vczvZKBFvDBBDT752UbwGW0k')
name = ''


@bot.message_handler(commands=['start'])
def greeting_table(message):
    bot.send_message(message.chat.id, "Приветствую в нашем боте")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Литье', callback_data='casting'))
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
        bot.send_message(call.message.chat.id, 'Выбрал зарплату сотрудников')
    elif call.data == 'products produced':
        bot.send_message(call.message.chat.id, 'Кто сколько положил на склад или отлил')

    elif call.data == 'customers':
        markup = telebot.types.InlineKeyboardMarkup()

        cursor.execute('SELECT * FROM Customers')

        while True:
            row = cursor.fetchone()
            if not row:
                break
            markup.add(telebot.types.InlineKeyboardButton(row[1], callback_data=f'customer_{row[0]}'))

        bot.send_message(call.message.chat.id, 'Выберите покупателя', reply_markup=markup)


# Применяем декоратор к функции обратного вызова
@bot.callback_query_handler(func=lambda call: True)
def callback_wrapper(call):
    my_callback(call)


# @connect_to_db
# def my_callback(call, conn, cursor):
#     if call.data == 'employees':
#         show_employees_table(bot, call)
#     elif call.data == 'employees list':
#         bot.send_message(call.message.chat.id, 'Выбрал список всех сотрудников')
#     elif call.data == 'salary':
#         bot.send_message(call.message.chat.id, 'Выбрал зарплату сотрудников')
#     elif call.data == 'products produced':
#         bot.send_message(call.message.chat.id, 'Кто сколько положил на склад или отлил')
#
#     elif call.data == 'customers':
#         markup = telebot.types.InlineKeyboardMarkup()
#
#         cursor.execute('SELECT * FROM Customers')
#
#         while True:
#             row = cursor.fetchone()
#             if not row:
#                 break
#             markup.add(telebot.types.InlineKeyboardButton(row[1], callback_data=f'customer_{row[0]}'))
#
#         bot.send_message(call.message.chat.id, 'Выберите покупателя', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_wrapper(call):
#     my_callback(call)


# @bot.callback_query_handler(func=lambda call: True)
# def employee_callback(call):
#     if call.data == 'employees list':
#         bot.send_message(call.message.chat.id, 'Выбрал список всех сотрудников')
#     elif call.data == 'salary':
#         bot.send_message(call.message.chat.id, 'Выбрал зарплату сотрудников')
#     elif call.data == 'products produced':
#         bot.send_message(call.message.chat.id, 'Кто сколько положил на склад или отлил')


# @bot.message_handler(commands=['add_customer'])
# def register_customer(message):
#     bot.send_message(message.chat.id, 'Регистрация нового покупателя\nВведите имя покупателя')
#
#     bot.register_next_step_handler(message, customer_name)
#
#
#
# def customer_name(message):
#     global name
#     name = message.text.strip()
#     sql_query = f"INSERT INTO Customers (Name) VALUES (?)"
#     values = (name)
#     con = pyodbc.connect(conStr)
#     cursor = con.cursor()
#     cursor.execute(sql_query, values)
#     con.commit()
#     con.close()
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton('Список покупателей', callback_data='employees'))
#     bot.send_message(message.chat.id, 'Покупатель добавлен', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     con = pyodbc.connect(conStr)
#     cursor = con.cursor()
#
#     cursor.execute('SELECT * FROM Customers')
#     users = cursor.fetchall()
#
#     info = ''
#     for user in users:
#         info += f"Имя: {user[1]}\n"
#
#     cursor.close()
#     con.close()
#
#     bot.send_message(call.message.chat.id, info)


#
#
# @bot.message_handler(commands=['customers'])
# def show_all_customers(message):
#     cursor.execute('SELECT * FROM Customers')
#
#     while 1:
#
#         row = cursor.fetchone()
#
#         if not row:
#             break
#
#         bot.send_message(message.chat.id, row.Name)
#
#
# @bot.message_handler(commands=['employees'])
# def show_all_employees(message):
#     cursor.execute('SELECT * FROM Employees')
#
#     while 1:
#
#         row = cursor.fetchone()
#
#         if not row:
#             break
#
#         bot.send_message(message.chat.id, row.Name)


# @bot.message_handler()
# def show_sql_query(message):
#     if "Select".lower() in message.text.lower():
#         query_result = show_db_query_data(message.text)
#
#         response = "\n".join(str(row) for row in query_result)
#
#         bot.send_message(message.chat.id, response)
#
#     elif "Insert".lower() in message.text.lower():
#         add_data_into_db(message.text)
#         bot.send_message(message.chat.id, message.text)


bot.polling(non_stop=True)
