import telebot
from telebot import TeleBot
from telebot import types

import pyodbc

from enum import Enum


def connect_db():
    con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])
    return pyodbc.connect(con_str)


def show_sales_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Сделать продажу', callback_data='sale products'))
    markup.add(telebot.types.InlineKeyboardButton('Посмотреть продажи', callback_data='show sales'))

    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)


def select_customer(chat_id, bot):
    conn = connect_db()
    cursor = conn.cursor()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cursor.execute('SELECT Name FROM Customers')
    rows = cursor.fetchall()
    for row in rows:
        markup.add(row[0])
    markup.add('Стоп')

    msg = bot.send_message(chat_id, 'Выберите покупателя', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda message: handle_customer(message, bot, conn))


def handle_customer(message, bot, conn):
    if message.text == 'Стоп':
        return

    cursor = conn.cursor()
    customer_name = message.text
    cursor.execute("select id from Customers where name = ?", customer_name)
    row = cursor.fetchone()
    customer_id = str(row[0])
    try:
        bot.send_message(message.chat.id, f"Вы выбрали: {customer_id}")

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        cursor.execute("SELECT Name FROM Products")
        rows = cursor.fetchall()
        for row in rows:
            markup.add(row[0])

        msg = bot.send_message(message.chat.id, 'Выберите товар', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda message: handle_product(message, bot, customer_id, conn))



    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


def handle_product(message, bot, customer_id, conn):
    product_name = message.text
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Products WHERE name = ?", product_name)
    row = cursor.fetchone()
    if row:
        product_id = row[0]
        msg = bot.send_message(message.chat.id, 'Введите количество: ')
        bot.register_next_step_handler(msg, lambda message: handle_amount_and_add(message, bot, customer_id, product_id,
                                                                                  conn))
    else:
        bot.send_message(message.chat.id, "Товар не найден")


def handle_amount_and_add(message, bot, customer_id, product_id, conn):
    amount = str(message.text)

    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Sales (CustomerId, ProductId, Amount) VALUES (?, ?, ?)",
                       (customer_id, product_id, amount))
        conn.commit()
        bot.send_message(message.chat.id, 'Продукция продана')
        select_customer(message.chat.id, bot)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    finally:
        conn.close()


def select_customer_for_show(chat_id, bot):
    conn = connect_db()
    cursor = conn.cursor()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cursor.execute('SELECT Name FROM Customers')
    rows = cursor.fetchall()
    for row in rows:
        markup.add(row[0])

    msg = bot.send_message(chat_id, 'Выберите покупателя', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda message: handle_customer_sale(message, bot, conn))


def handle_customer_sale(message, bot, conn):
    customer_id = message.text
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
              'Декабрь']

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for month in months:
        markup.add(types.KeyboardButton(month))

    msg = bot.send_message(message.chat.id, 'Выберите месяц', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda message: show_customer_sales(message, bot, conn, customer_id, months))


def show_customer_sales(message, bot, conn, customer_id: str, months: list):
    month = message.text

    cursor = conn.cursor()

    try:
        query = """
            SELECT c.Name, 
                   p.Name, 
                   s.Amount, 
                   s.Sale_Date, 
                   s.Amount * p.Our_sale_price AS Price, 
                   SUM(s.Amount * p.Our_sale_price) OVER () AS TotalSum
            FROM Sales s
            INNER JOIN Customers c ON s.CustomerId = c.Id
            JOIN Products p ON s.ProductId = p.Id
            WHERE c.Name = ? AND MONTH(s.Sale_Date) = ?
        """
        cursor.execute(query, (customer_id, months.index(month) + 1))

        results = cursor.fetchall()

        if results:
            sales_message = f'Продажи {customer_id} за {month}:\n'
            sales_message += f'Дата: {results[0][3]}\n'
            for row in results:
                sales_message += f'{row[1]} {row[2]}шт\n'
            sales_message += f'Общая сумма: {results[0][5]}'
            bot.send_message(message.chat.id, sales_message)
        else:
            bot.send_message(message.chat.id, f'Продажи {customer_id} за {month} не найдены')

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    finally:
        conn.close()
