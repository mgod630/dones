import enum
import time
from flask import current_app as app
import mysql.connector.pooling
from routes import common

connection_pool = None


class Users:
    @staticmethod
    def get_all_users():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_users ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_all_users_reverse():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_users ORDER BY id DESC")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_user_by_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_users WHERE id=%(id)s"
        cursor.execute(query, {'id': user_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_user_by_g_token(g_token):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_users WHERE g_token=%(g_token)s"
        cursor.execute(query, {'g_token': g_token})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_user_by_mobile_and_password(mobile, password):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_users WHERE mobile=%(mobile)s"
        cursor.execute(query, {'mobile': mobile})
        row = cursor.fetchone()
        cnx.close()
        user = None
        if common.check_password(password, row['password']):
            user = row
        return user
    
    @staticmethod
    def get_user_by_mobile(mobile):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_users WHERE mobile=%(mobile)s"
        cursor.execute(query, {'mobile': mobile})
        row = cursor.fetchone()
        cnx.close()
        user = row
        return user

    @staticmethod
    def get_users_count():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = 'SELECT COUNT(id) FROM tbl_users;'
        cursor.execute(query)
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user(full_name='empty', mobile='empty', g_token='empty', password='empty', user_type=0, register_datetime=0, registering_code=0):
        password = common.get_hashed_password(password)
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_users` (`full_name`, `mobile`, `g_token`, `password`, `user_type`, `register_datetime`, `registering_code`) VALUES" +
                    "( %(full_name)s, %(mobile)s, %(g_token)s, %(password)s, %(user_type)s, %(register_datetime)s, %(registering_code)s)")
        data_user = {
            'full_name': full_name,
            'mobile': mobile,
            'g_token': g_token,
            'password': password,
            'user_type': user_type,
            'register_datetime': register_datetime,
            'registering_code': registering_code
        }

        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        
        return inserted_record_id

    @staticmethod
    def update_user(id, full_name=None, mobile=None, password=None, user_type=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        if password:
            password = common.get_hashed_password(password)
        update_string = ''
        if full_name:
            update_string += f'full_name = %(full_name)s,'
        if mobile:
            update_string += f'mobile=%(mobile)s,'
        if password:
            update_string += f'password=%(password)s,'
        if user_type:
            update_string += f'user_type=%(user_type)s,'
        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_users SET {update_string} WHERE id='{id}'"
        update_query_string = {
            'full_name': full_name,
            'mobile': mobile,
            'password': password,
            'user_type': user_type,
        }
        cursor.execute(add_user, update_query_string)
        cnx.commit()
        cnx.close()
        return True

    # delete
    @staticmethod
    def delete_all_users():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_users')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_user_by_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = 'DELETE FROM tbl_users WHERE id = %(id)s'
        cursor.execute(query, {'id': user_id})
        cnx.commit()
        cnx.close()
        return True

    class Types(enum.Enum):
        blocked_user = enum.auto()
        new_user = 0
        verified_customer = enum.auto()
        system_user = enum.auto()
        admin = enum.auto()
        super_admin = enum.auto()

def users_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Users.insert_new_user(f'name{i}', f'mobile{i}', f'g_token{i}', f'password{i}',
                                    f'sheba_number{i}', i, Users.Types.new_user, f'{i*11}', time.time())
    update = Users.update_user(last_id, full_name=f'Updated_full_name{i}')
    last_record = Users.get_user_by_id(last_id)
    print(last_record)
    print('-' * 80)
    all_records = Users.get_all_users()
    print(all_records)


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    users_orm_functions_test()
    print('Everything is alright!')