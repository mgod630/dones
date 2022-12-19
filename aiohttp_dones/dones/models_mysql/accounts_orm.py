import enum
import mysql.connector.pooling
from flask import current_app as app
from models_mysql import transactions_orm

connection_pool = None


class Accounts:
    @staticmethod
    def get_all_accounts():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_accounts ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_account_by_id(account_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_accounts WHERE id='%(id)s'"
        cursor.execute(query, {'id': account_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_account_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_accounts WHERE user_id='%(user_id)s'"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_account(user_id, account_type, rial_balance=0, gold_18k_balance=0, rial_blocked=0, gold_18k_blocked=0):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_account = ("INSERT INTO `tbl_accounts` (`user_id`, `account_type`, `rial_balance`, `gold_18k_balance`, `rial_blocked`, `gold_18k_blocked`) VALUES" +
                       "( %(user_id)s, %(account_type)s, %(rial_balance)s, %(gold_18k_balance)s, %(rial_blocked)s, %(gold_18k_blocked)s)")
        data_account = {
            'user_id': user_id,
            'account_type': account_type.value,
            'rial_balance': rial_balance,
            'gold_18k_balance': gold_18k_balance,
            'rial_blocked': rial_blocked,
            'gold_18k_blocked': gold_18k_blocked,
        }
        cursor.execute(add_account, data_account)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_account(id, user_id=None, account_type=None, rial_balance=None, gold_18k_balance=None, rial_blocked=None, gold_18k_blocked=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if user_id:
            update_string += f'user_id = %(user_id)s,'
        if account_type:
            update_string += f'account_type=%(account_type)s,'
        if rial_balance:
            update_string += f'rial_balance=%(rial_balance)s,'
        if gold_18k_balance:
            update_string += f'gold_18k_balance=%(gold_18k_balance)s,'
        if rial_blocked:
            update_string += f'rial_blocked=%(rial_blocked)s,'
        if gold_18k_blocked:
            update_string += f'gold_18k_blocked=%(gold_18k_blocked)s,'
        update_string = update_string.rstrip(',')
        add_account = f"UPDATE tbl_accounts SET {update_string} WHERE id='{id}'"
        data_account = {
            'user_id': user_id,
            'account_type': account_type.value,
            'rial_balance': rial_balance,
            'gold_18k_balance': gold_18k_balance,
            'rial_blocked': rial_blocked,
            'gold_18k_blocked': gold_18k_blocked,
        }
        cursor.execute(add_account, data_account)
        cnx.commit()
        cnx.close()
        return True

    def buy_or_sell_gold_transaction(transaction_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            get_and_lock_user_transaction_row = 'SELECT * FROM tbl_transactions WHERE id="%(id)s" FOR UPDATE'
            data = {'id': transaction_id}
            cursor.execute(get_and_lock_user_transaction_row, data)
            transaction = cursor.fetchone()
            get_and_lock_user_account_row = 'SELECT * FROM tbl_accounts WHERE id="%(id)s" FOR UPDATE'
            data = {'id': transaction['account_id']}
            cursor.execute(get_and_lock_user_account_row, data)
            user_account = cursor.fetchone()
            rial_amount = transaction['amount'] * \
                transaction['asset_price_at_transaction_time']
            if transaction['amount'] > 0 and ((transaction['transaction_type'] == transactions_orm.Transactions.Types.buy_token.value and user_account['rial_balance'] >= rial_amount) or (transaction['transaction_type'] == transactions_orm.Transactions.Types.sell_token.value and user_account['gold_18k_balance'] >= transaction['amount'])):
                if transaction['transaction_type'] == transactions_orm.Transactions.Types.buy_token.value:
                    account_update_query_string = 'UPDATE tbl_accounts SET rial_balance = rial_balance - %(rial_amount)s, gold_18k_balance = gold_18k_balance + %(gold_amount)s WHERE id="%(account_id)s"'
                    asset_update_query_string = 'UPDATE tbl_assets SET trade_limit_percentage_index = trade_limit_percentage_index - %(amount)s WHERE id="%(id)s"'
                elif transaction['transaction_type'] == transactions_orm.Transactions.Types.sell_token.value:
                    account_update_query_string = 'UPDATE tbl_accounts SET rial_balance = rial_balance + %(rial_amount)s, gold_18k_balance = gold_18k_balance - %(gold_amount)s WHERE id="%(account_id)s"'
                    asset_update_query_string = 'UPDATE tbl_assets SET trade_limit_percentage_index = trade_limit_percentage_index + %(amount)s WHERE id="%(id)s"'
                data = {'account_id': transaction['account_id'],
                        'rial_amount': rial_amount, 'gold_amount': transaction['amount']}
                cursor.execute(account_update_query_string, data)
                transaction_update_query_string = 'UPDATE tbl_transactions SET status = %(status)s WHERE id="%(id)s"'
                data = {'id': transaction_id,
                        'status': transactions_orm.Transactions.Status.successful.value}
                cursor.execute(transaction_update_query_string, data)
                data = {'id': transaction['asset_id'],
                        'amount': transaction['amount']}
                cursor.execute(asset_update_query_string, data)
            cnx.commit()
        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            cnx.rollback()  # reverting changes because of exception
        finally:
            if cnx.is_connected():
                cnx.close()

    class Types(enum.Enum):
        A = enum.auto()
        B = enum.auto()

# class Account_types:
#     @staticmethod
#     def get_all_account_types():
#         global connection_pool
#         if connection_pool == None: connection_pool = app.config['mysql_connection_pool']
#         cnx = connection_pool.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         query = ("SELECT * FROM tbl_account_types ")
#         cursor.execute(query)
#         data = cursor.fetchall()
#         cnx.close()
#         return data

#     @staticmethod
#     def get_account_type_by_id(account_type_id):
#         global connection_pool
#         if connection_pool == None: connection_pool = app.config['mysql_connection_pool']
#         cnx = connection_pool.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         query = "SELECT * FROM tbl_account_types WHERE id='%(id)s'"
#         cursor.execute(query, {'id':account_type_id})
#         row = cursor.fetchone()
#         cnx.close()
#         return row

#     @staticmethod
#     def get_account_type_by_description(description):
#         global connection_pool
#         if connection_pool == None: connection_pool = app.config['mysql_connection_pool']
#         cnx = connection_pool.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         query = "SELECT * FROM tbl_account_types WHERE description=%(description)s"
#         cursor.execute(query, {'description':description})
#         row = cursor.fetchone()
#         cnx.close()
#         return row

#     @staticmethod
#     def insert_new_account_type(title, description):
#         global connection_pool
#         if connection_pool == None: connection_pool = app.config['mysql_connection_pool']
#         cnx = connection_pool.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         add_account_type = ("INSERT INTO `tbl_account_types` (`title`, `description`) VALUES" +
#                             "( %(title)s, %(description)s)")
#         data_account_type = {
#         'title': title,
#         'description': description,
#         }
#         cursor.execute(add_account_type, data_account_type)
#         inserted_record_id = cursor.lastrowid
#         cnx.commit()
#         cnx.close()
#         return inserted_record_id

#     @staticmethod
#     def update_account_type(id, title = None, description= None):
#         global connection_pool
#         if connection_pool == None: connection_pool = app.config['mysql_connection_pool']
#         cnx = connection_pool.get_connection()
#         cursor = cnx.cursor()
#         update_string = ''
#         if title: update_string += f'title = %(title)s,'
#         if description: update_string += f'description=%(description)s,'
#         update_string = update_string.rstrip(',')
#         add_account_type = f"UPDATE tbl_account_types SET {update_string} WHERE id='{id}'"
#         data_account_type = {
#         'title': title,
#         'description': description,
#         }
#         cursor.execute(add_account_type, data_account_type)
#         cnx.commit()
#         cnx.close()
#         return True

# def account_types_orm_functions_test():
#     import random
#     i = random.randint(1,1000)
#     last_id = Account_types.insert_new_account_type(f'title{i}', f'description{i}')
#     update = Account_types.update_account_type(last_id, title=f'Updated_title{i}')
#     last_account_type = Account_types.get_account_type_by_id(last_id)
#     print(last_account_type)
#     print('-' * 80)
#     all_account_types = Account_types.get_all_account_types()
#     print(all_account_types)
#     return True


def accounts_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Accounts.insert_new_account(i, i, i, i, i, i)
    update = Accounts.update_account(last_id, user_id=i*2)
    last_account = Accounts.get_account_by_id(last_id)
    print(last_account)
    print('-' * 80)
    all_accounts = Accounts.get_all_accounts()
    print(all_accounts)


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    accounts_orm_functions_test()
    # account_types_orm_functions_test()
    print('Everything is alright!')
