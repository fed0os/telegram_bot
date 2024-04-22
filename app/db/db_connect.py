import pyodbc

driver = 'DRIVER={SQL Server}'
server = 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01'
db = 'DATABASE=LEDA'


def connect_to_db(func):
    def wrapper(*args, **kwargs):
        con_str = ';'.join(['DRIVER={SQL Server}', 'SERVER=WIN-IUA2D70C19F\MSSQLSERVER01', 'DATABASE=LEDA'])

        conn = pyodbc.connect(con_str)
        cursor = conn.cursor()

        result = func(conn, cursor, *args, **kwargs)

        conn.close()

        return result

    return wrapper

