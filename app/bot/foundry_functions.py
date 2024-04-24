import telebot
from telebot import TeleBot

from storage_functions import show_information


def show_foundry_table(tel_bol: TeleBot, call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Деталей не обработанно', callback_data='No details processed'))
    markup.add(telebot.types.InlineKeyboardButton('Добавить детали', callback_data='Add details'))
    tel_bol.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=markup)


def show_no_processed_details(tel_bot: TeleBot, call, cursor):
    query = """SELECT 
                    p.Name, 
                      CASE
                    WHEN Foundry.TotalAmount - Processed.TotalAmount < 0 THEN 0
                    ELSE Foundry.TotalAmount - Processed.TotalAmount
                END AS Difference
                FROM (
                    SELECT ProductId, SUM(Amount) AS TotalAmount
                    FROM Foundry_product
                    GROUP BY ProductId
                ) AS Foundry
                
                JOIN (
                    SELECT ProductId, SUM(Amount) AS TotalAmount
                    FROM Processed_product
                    WHERE DateColumn > '2024-04-16'
                    GROUP BY ProductId
                ) AS Processed ON Foundry.ProductId = Processed.ProductId
                join Products p on Foundry.ProductId = p.Id
                """

    show_information(query, cursor, tel_bot, call)


