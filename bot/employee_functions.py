import telebot
from telebot import TeleBot



def show_employees_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список сотрудников', callback_data='employees list'))
    markup.add(telebot.types.InlineKeyboardButton('Зп сотрудника', callback_data='salary'))
    markup.add(telebot.types.InlineKeyboardButton('Сколько положил на склад', callback_data='products produced'))
    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)


def show_all_employee(tel_bot: TeleBot, call, cursor):
    cursor.execute('SELECT * FROM Employees')
    info = ''
    while True:
        row = cursor.fetchone()
        if not row:
            break
        info += f"Имя: {str(row[1])}\n"
    tel_bot.send_message(call.message.chat.id, info)