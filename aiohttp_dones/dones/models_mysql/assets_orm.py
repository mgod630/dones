from flask import current_app as app
import mysql.connector.pooling

connection_pool = None


class Assets:
    @staticmethod
    def get_all_assets():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_assets ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_asset_by_id(asset_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_assets WHERE id='%(id)s'"
        cursor.execute(query, {'id': asset_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_asset_by_code(code):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_assets WHERE code=%(code)s"
        cursor.execute(query, {'code': code})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_asset(title, code, unit_fa, image_path, description, buy_price, sell_price, daily_buy_limit, daily_sell_limit, trade_limit_percentage_index):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_asset = ("INSERT INTO `tbl_assets` (`title`, `code`, `unit_fa`, `image_path`, `description`, `buy_price`, `sell_price`, `daily_buy_limit`, `daily_sell_limit`, `trade_limit_percentage_index`) VALUES" +
                     "( %(title)s, %(code)s, %(unit_fa)s, %(image_path)s, %(description)s, %(buy_price)s, %(sell_price)s, %(daily_buy_limit)s, %(daily_sell_limit)s, %(trade_limit_percentage_index)s)")
        data_asset = {
            'title': title,
            'code': code,
            'unit_fa': unit_fa,
            'image_path': image_path,
            'description': description,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'daily_buy_limit': daily_buy_limit,
            'daily_sell_limit': daily_sell_limit,
            'trade_limit_percentage_index': trade_limit_percentage_index,
        }
        cursor.execute(add_asset, data_asset)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_asset(id, title=None, code=None, unit_fa=None, image_path=None, description=None, buy_price=None, sell_price=None, daily_buy_limit=None, daily_sell_limit=None, trade_limit_percentage_index=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if title:
            update_string += f'title = %(title)s,'
        if code:
            update_string += f'code=%(code)s,'
        if unit_fa:
            update_string += f'unit_fa=%(unit_fa)s,'
        if image_path:
            update_string += f'image_path=%(image_path)s,'
        if description:
            update_string += f'description=%(description)s,'
        if buy_price:
            update_string += f'buy_price=%(buy_price)s,'
        if sell_price:
            update_string += f'sell_price=%(sell_price)s,'
        if daily_buy_limit:
            update_string += f'daily_buy_limit=%(daily_buy_limit)s,'
        if daily_sell_limit:
            update_string += f'daily_sell_limit=%(daily_sell_limit)s,'
        if trade_limit_percentage_index:
            update_string += f'trade_limit_percentage_index=%(trade_limit_percentage_index)s,'
        update_string = update_string.rstrip(',')
        add_asset = f"UPDATE tbl_assets SET {update_string} WHERE id='{id}'"
        data_asset = {
            'title': title,
            'code': code,
            'unit_fa': unit_fa,
            'image_path': image_path,
            'description': description,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'daily_buy_limit': daily_buy_limit,
            'daily_sell_limit': daily_sell_limit,
            'trade_limit_percentage_index': trade_limit_percentage_index,
        }
        cursor.execute(add_asset, data_asset)
        cnx.commit()
        cnx.close()
        return True


def assets_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Assets.insert_new_asset(
        f'title{i}', f'code{i}', f'unit_fa{i}', f'image_path{i}', f'description{i}', i, 0, f'{i*11}', i, i)
    update = Assets.update_asset(last_id, title=f'Updated_title{i}')
    last_asset = Assets.get_asset_by_id(last_id)
    print(last_asset)
    print('-' * 80)
    all_assets = Assets.get_all_assets()
    print(all_assets)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    assets_orm_functions_test()
    print('Everything is alright!')
