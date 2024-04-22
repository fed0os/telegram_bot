import telebot
from telebot import TeleBot


def show_aluminium_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Остаток алюминия', callback_data='aluminium residue'))
    markup.add(telebot.types.InlineKeyboardButton('Добавить алюминий', callback_data='add aluminium'))

    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)

def show_aluminium_residue(tel_bol: TeleBot, call, cursor):

    query = """
                SELECT (
            (SELECT SUM(Amount) FROM Aluminium) - 
            (SELECT SUM(fp.Amount * p.Weight) AS total_sum 
             FROM Foundry_product fp
             INNER JOIN Products p ON fp.ProductId = p.Id 
             WHERE fp.EmployeeId <> 24)
        ) AS total;

        """

    cursor.execute(query)

    info = ''

    while 1:
        row = cursor.fetchone()
        if not row:
            break
        info += f'Осталось {int(row[0])} кг'
        tel_bol.send_message(call.message.chat.id, info)