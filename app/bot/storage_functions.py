import telebot
from telebot import TeleBot


def show_information(query, cursor_info, bot: TeleBot, call):
    cursor_info.execute(query)
    info = ''
    while True:
        row = cursor_info.fetchone()
        if not row:
            break
        info += f"{str(row[0])}   {int(row[1])} шт \n"
    bot.send_message(call.message.chat.id, info)


def show_storage_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Наш склад', callback_data='our storage'))
    markup.add(telebot.types.InlineKeyboardButton('Димы склад', callback_data='dima storage'))

    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)


def show_our_storage(tel_bot: TeleBot, call, cursor):
    query = """SELECT 
                p.Name AS ProductName,
                COALESCE(pp.TotalAmount, 0) - COALESCE(dw.TotalAmount, 0) - COALESCE(s.Amount, 0) AS Difference
            FROM (
                SELECT ProductId, SUM(Amount) AS TotalAmount
                FROM Dima_warehouse
                GROUP BY ProductId
            ) dw
            LEFT JOIN (
                SELECT ProductId, SUM(Amount) AS TotalAmount
                FROM Processed_product
                GROUP BY ProductId
            ) pp ON dw.ProductId = pp.ProductId
            JOIN Products p ON dw.ProductId = p.Id
            LEFT JOIN (
                SELECT ProductId, SUM(Amount) AS Amount
                FROM Sales
                WHERE CustomerId != 4
                GROUP BY ProductId
            ) s ON p.Id = s.ProductId;"""

    show_information(query, cursor, tel_bot, call)


def show_dima_storage(tel_bot: TeleBot, call, cursor):
    query = """SELECT 
                p.Name, 
                SUM(dw.Amount) - COALESCE(SUM(s.Amount), 0) AS total_amount
            FROM 
                Dima_warehouse dw
            JOIN 
                Products p ON dw.ProductId = p.Id
            LEFT JOIN 
                Sales s ON dw.ProductId = s.ProductId and s.CustomerId = 4
            GROUP BY 
                p.Name;"""

    show_information(query, cursor, tel_bot, call)
