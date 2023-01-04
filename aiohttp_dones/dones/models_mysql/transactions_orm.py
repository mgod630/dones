import enum
import time
from datetime import datetime
import mysql.connector.pooling
from flask import current_app as app

connection_pool = None

class Transactions:
    @staticmethod
    def get_all_transactions():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_transactions ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_all_transactions_reverse_with_users():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ('''SELECT t.*, u.full_name, u.mobile 
                    FROM tbl_transactions t 
                    INNER JOIN tbl_users u
                    ON u.id = t.user_id
                    ORDER BY t.id DESC''')
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_transaction_by_id(transaction_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE id=%(id)s"
        cursor.execute(query, {'id': transaction_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_transaction_by_ipg_id(ipg_ref_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE ipg_ref_id=%(ipg_ref_id)s"
        cursor.execute(query, {'ipg_ref_id': ipg_ref_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_transaction_by_course_id(course_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE course_id=%(course_id)s"
        cursor.execute(query, {'course_id': course_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_transaction_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE user_id=%(user_id)s"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_last_rowid():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute('SELECT id FROM tbl_transactions ORDER BY id DESC LIMIT 1;') 
        last_rowid = cursor.fetchone()
        cnx.close()
        return last_rowid

    @staticmethod
    def insert_new_transaction(user_id, course_id, amount, create_datetime, transaction_type, status, ipg_ref_id, fs_invoice_number, description, ipg_invoice_number=0):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_transaction = ("INSERT INTO `tbl_transactions` (`user_id`, `course_id`, `amount`, `create_datetime`, `transaction_type`, `status`, `ipg_ref_id`, `description`, `fs_invoice_number`, `ipg_invoice_number`) VALUES" +
                           "( %(user_id)s, %(course_id)s, %(amount)s, %(create_datetime)s, %(transaction_type)s, %(status)s, %(ipg_ref_id)s, %(description)s, %(fs_invoice_number)s, %(ipg_invoice_number)s)")
        data_transaction = {
            'user_id': user_id,
            'course_id': course_id,
            'amount': amount,
            'create_datetime': create_datetime,
            'transaction_type': transaction_type,
            'status': status,
            'ipg_ref_id': ipg_ref_id,
            'description': description,
            'ipg_invoice_number': ipg_invoice_number,
            'fs_invoice_number': fs_invoice_number
        }
        cursor.execute(add_transaction, data_transaction)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_transaction(id, user_id=None, course_id=None, amount=None, create_datetime=None, transaction_type=None, status=None, ipg_ref_id=None, description=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if user_id:
            update_string += f'user_id = %(user_id)s,'
        if course_id:
            update_string += f'course_id=%(course_id)s,'
        if amount:
            update_string += f'amount=%(amount)s,'
        if create_datetime:
            update_string += f'create_datetime=%(create_datetime)s,'
        if transaction_type:
            update_string += f'transaction_type=%(transaction_type)s,'
        if status:
            update_string += f'status=%(status)s,'
        if ipg_ref_id:
            update_string += f'ipg_ref_id=%(ipg_ref_id)s,'
        if description:
            update_string += f'description=%(description)s,'
        update_string = update_string.rstrip(',')
        add_transaction = f"UPDATE tbl_transactions SET {update_string} WHERE id='{id}'"
        data_transaction = {
            'user_id': user_id,
            'course_id': course_id,
            'amount': amount,
            'create_datetime': create_datetime,
            'transaction_type': transaction_type,
            'status': status,
            'ipg_ref_id': ipg_ref_id,
            'description': description,
        }
        cursor.execute(add_transaction, data_transaction)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def update_transaction_by_ipg_id(ipg_ref_id, ipg_invoice_number=None, create_datetime=None, transaction_type=None, status=None, description=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if create_datetime:
            update_string += f'create_datetime=%(create_datetime)s,'
        if transaction_type:
            update_string += f'transaction_type=%(transaction_type)s,'
        if status:
            update_string += f'status=%(status)s,'
        if description:
            update_string += f'description=%(description)s,'
        if ipg_invoice_number:
            update_string += f'ipg_invoice_number=%(ipg_invoice_number)s'
        update_string = update_string.rstrip(',')
        add_transaction = f"UPDATE tbl_transactions SET {update_string} WHERE ipg_ref_id='{ipg_ref_id}'"
        data_transaction = {
            'create_datetime': create_datetime,
            'transaction_type': transaction_type,
            'status': status,
            'description': description,
            'ipg_invoice_number': ipg_invoice_number
        }
        cursor.execute(add_transaction, data_transaction)
        cnx.commit()
        cnx.close()
        return True

    class Status(enum.Enum):
        Unknown = enum.auto()
        successful = enum.auto()
        failed = enum.auto()
        pending = enum.auto()
        expired = enum.auto()
        queued = enum.auto()
        canceling = enum.auto()
        canceled = enum.auto()

    class Types(enum.Enum):
        ipg_cash_deposit = enum.auto()
        admin_cash_deposit = enum.auto()
        gift_cash_deposit = enum.auto()
        buy_token = enum.auto()

def transactions_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Transactions.insert_new_transaction(i, i, i, time.time(
    ), Transactions.Types.buy_token, Transactions.Status.pending, 0, f'{i*11}')
    update = Transactions.update_transaction(last_id, user_id=i*2)
    last_transaction = Transactions.get_transaction_by_id(last_id)
    print(last_transaction)
    print('-' * 80)
    all_transactions = Transactions.get_all_transactions()
    print(all_transactions)


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    transactions_orm_functions_test()
    print('Everything is alright!')
