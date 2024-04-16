import pyodbc

driver = 'DRIVER={SQL Server}'
server = 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01'
db = 'DATABASE=LEDA'


def connect_to_db(func):
    def wrapper(*args, **kwargs):
        con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])

        conn = pyodbc.connect(con_str)
        cursor = conn.cursor()

        # Вызываем декорируемую функцию с соединением и курсором
        result = func(conn, cursor, *args, **kwargs)

        conn.close()

        return result

    return wrapper

# @connect_to_db
# def my_function(conn, cursor):
#     cursor.execute('SELECT * FROM Employees')
#
#
#     while 1:
#         rows = cursor.fetchone()
#         if not rows:
#             break
#         print(rows[1])
#
# # Вызов функции
# my_function()