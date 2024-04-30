import logging
from telebot import TeleBot, types
from app.db.db_connect import connect_to_db
from employee_functions import show_employees_table, show_all_employee, show_employees_salary
from foundry_functions import show_foundry_table, show_no_processed_details
from storage_functions import show_storage_table, show_our_storage, show_dima_storage
from aluminium import show_aluminium_residue, show_aluminium_table
from add_foundry_products import add_foundry_product
from add_process_product import add_process_product
from sales import show_sales_table, select_customer, select_customer_for_show

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

driver = 'DRIVER={SQL Server}'
server = 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01'
db = 'DATABASE=LEDA'

bot = TeleBot('6601289362:AAHP8IfBXJ4vczvZKBFvDBBDT752UbwGW0k')


def log_info(message):
    logger.info("User {} - {}".format(message.from_user.id, message.text))


@bot.message_handler(commands=['start'])
def greeting_table(message):
    bot.send_message(message.chat.id, "Приветствую в нашем боте")
    log_info(message)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Литье', callback_data='casting'))
    markup.add(types.InlineKeyboardButton('Метал', callback_data='aluminium'))
    markup.add(types.InlineKeyboardButton('Склад', callback_data='storage'))
    markup.add(types.InlineKeyboardButton('Продажи', callback_data='sales'))
    markup.add(types.InlineKeyboardButton('Сотрудники', callback_data='employees'))
    bot.send_message(message.chat.id, 'Выберите пункт', reply_markup=markup)


@connect_to_db
def my_callback(conn, cursor, call):
    if call.data == 'employees':
        show_employees_table(bot, call)

    elif call.data == 'employees list':
        show_all_employee(bot, call, cursor)
    elif call.data == 'salary':
        show_employees_salary(bot, call, cursor)

    if call.data == 'aluminium':
        show_aluminium_table(bot, call)
    elif call.data == 'aluminium residue':
        show_aluminium_residue(bot, call, cursor)

    if call.data == 'casting':
        show_foundry_table(bot, call)
    elif call.data == 'No details processed':
        show_no_processed_details(bot, call, cursor)
    elif call.data == 'Add details':
        add_foundry_product(call.message.chat.id, cursor, bot)

    if call.data == 'storage':
        show_storage_table(bot, call)
    elif call.data == 'our storage':
        show_our_storage(bot, call, cursor)
    elif call.data == 'dima storage':
        show_dima_storage(bot, call, cursor)
    elif call.data == 'products produced':
        add_process_product(call.message.chat.id, cursor, bot)

    if call.data == 'sales':
        show_sales_table(bot, call)
    elif call.data == 'sale products':
        select_customer(call.message.chat.id, bot)
    elif call.data == 'show sales':
        select_customer_for_show(call.message.chat.id, bot)

    log_info(call.message)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    my_callback(call)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    bot.send_message(message.chat.id, "Неизвестная команда. Пожалуйста, используйте команду /start.")
    logger.warning("Unknown command received from user {}".format(message.from_user.id))
    log_info(message)


if __name__ == '__main__':

    bot.infinity_polling()
