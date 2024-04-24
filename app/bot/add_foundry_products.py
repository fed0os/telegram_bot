import pyodbc

from telebot import types

product_id = ''
employee_id = ''
amount = ''


def add_foundry_product(chat_id, cursor, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cursor.execute('SELECT Name FROM Products')
    rows = cursor.fetchall()
    for row in rows:
        markup.add(row[0])  # Добавляем название товара в клавиатуру

    msg = bot.send_message(chat_id, 'Выберите товар', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda message: handle_product(message, cursor, bot))


def handle_product(message, cursor, bot):
    global product_id

    con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])
    conn = pyodbc.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(f"select id from Products where name = '{message.text}'")
    row = cursor.fetchone()
    product_id = str(row[0])
    try:
        bot.send_message(message.chat.id, f"Вы выбрали товар: {product_id}")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cursor.execute("SELECT Name FROM Employees WHERE Name <> 'Начальное значение' AND Job_title <> 'Слесарь'")
        rows = cursor.fetchall()
        for row in rows:
            markup.add(row[0])

        conn.close()
        msg = bot.send_message(message.chat.id, 'Выберите сотрудника', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda message: handle_employee(message, bot))



    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


def handle_employee(message, bot):
    global employee_id

    con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])
    conn = pyodbc.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(f"select id from Employees where name = '{message.text}'")
    row = cursor.fetchone()
    employee_id = str(row[0])
    conn.close()
    try:

        msg = bot.send_message(message.chat.id, 'Выберите колличество: ')
        bot.register_next_step_handler(msg, lambda message: handle_amount_and_add(message, bot))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


def handle_amount_and_add(message, bot):
    global amount
    amount = str(message.text)

    msg = bot.send_message(message.chat.id, f'Ты ввел {amount}')
    con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])
    conn = pyodbc.connect(con_str)
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"INSERT INTO Foundry_product (EmployeeId, ProductId, Amount) VALUES ('{employee_id}', '{product_id}', '{amount}')")

        conn.commit()  # Commit the transaction

        bot.send_message(message.chat.id, 'Продукция добавлена')

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    finally:
        conn.close()
