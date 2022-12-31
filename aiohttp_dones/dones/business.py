import mysql.connector.pooling
from models_mysql import transactions_orm, assets_orm, accounts_orm
from date_converter.datetime_converter import Datetime_converter
from flask import current_app as app

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
transactions_orm.connection_pool = accounts_orm.connection_pool = assets_orm.connection_pool = connection_pool


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


gold_asset = assets_orm.Assets.get_asset_by_id(1)
user1_account = accounts_orm.Accounts.get_account_by_id(1)
amount_gram = 0.001
transaction_time = Datetime_converter.now_mysql_ready()
transaction_type = transactions_orm.Transactions.Types.buy_token
asset_price = None
if transaction_type == transactions_orm.Transactions.Types.buy_token:
    asset_price = gold_asset['buy_price']
if transaction_type == transactions_orm.Transactions.Types.sell_token:
    asset_price = gold_asset['sell_price']
new_tr_id = transactions_orm.Transactions.insert_new_transaction(
    user1_account['id'], gold_asset['id'], amount_gram, transaction_time, transaction_type, transactions_orm.Transactions.Status.pending, asset_price, 'Buy')
transaction = transactions_orm.Transactions.get_transaction_by_id(new_tr_id)
if transaction['transaction_type'] in (transactions_orm.Transactions.Types.buy_token.value, transactions_orm.Transactions.Types.sell_token.value):
    buy_or_sell_gold_transaction(transaction['id'])
print('Salam...')
