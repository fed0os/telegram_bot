import telebot
from telebot import TeleBot


def show_employees_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список сотрудников', callback_data='employees list'))
    markup.add(telebot.types.InlineKeyboardButton('Зп сотрудника', callback_data='salary'))
    markup.add(telebot.types.InlineKeyboardButton('Сколько положил на склад', callback_data='products produced'))
    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)


def show_all_employee(tel_bot: TeleBot, call, cursor):
    cursor.execute("SELECT * FROM Employees where Name <> 'Начальное значение'")
    info = ''
    while True:
        row = cursor.fetchone()
        if not row:
            break
        info += f"Имя: {str(row[1])}\n"
    tel_bot.send_message(call.message.chat.id, info)


def show_employees_salary(tel_bot: TeleBot, call, cursor):
    query = """SELECT e.Name, SUM(fp.Amount * p.Foundry_product_price) AS total
            FROM Foundry_product fp
            JOIN Products p ON fp.ProductId = p.id
            JOIN Employees e ON fp.EmployeeId = e.id
            WHERE e.Name <> 'Начальное значение' AND fp.DateColumn BETWEEN '2024-04-16' AND '2024-04-30'
            GROUP BY e.Name
            UNION ALL
            SELECT e.Name, SUM(pp.Amount * p.Processed_product_price) AS total
            FROM Processed_product pp
            JOIN Products p ON pp.ProductId = p.id
            JOIN Employees e ON pp.EmployeeId = e.id
            WHERE e.Name <> 'Начальное значение' AND pp.DateColumn BETWEEN '2024-04-16' AND '2024-04-30'
            GROUP BY e.Name;"""

    cursor.execute(query)
    info = ''
    while True:
        row = cursor.fetchone()
        if not row:
            break
        info += f"Имя: {str(row[0])}   Зп: {int(row[1])}\n"
    tel_bot.send_message(call.message.chat.id, info)
