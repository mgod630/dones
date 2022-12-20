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
    def get_user_by_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_users WHERE id='%(id)s'"
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
    def insert_new_user(full_name, mobile, g_token, password, national_id, sheba_number, credit_score, user_type, invited_friend_mobile, register_datetime):
        password = common.get_hashed_password(password)
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_users` (`full_name`, `mobile`, `g_token`, `password`, `sheba_number`, `credit_score`, `user_type`, `invited_friend_mobile`, `register_datetime`, `national_id`) VALUES" +
                    "( %(full_name)s, %(mobile)s, %(g_token)s, %(password)s, %(sheba_number)s, %(credit_score)s, %(user_type)s, %(invited_friend_mobile)s, %(register_datetime)s, %(national_id)s)")
        data_user = {
            'full_name': full_name,
            'mobile': mobile,
            'g_token': g_token,
            'password': password,
            'sheba_number': sheba_number,
            'credit_score': credit_score,
            'user_type': user_type,
            'invited_friend_mobile': invited_friend_mobile,
            'register_datetime': register_datetime,
            'national_id': national_id,
        }
        try:
            cursor.execute(add_user, data_user)
            inserted_record_id = cursor.lastrowid
            cnx.commit()
            cnx.close()
        except:
            print('mysql error')
        return inserted_record_id

    @staticmethod
    def update_user(id, full_name=None, mobile=None, password=None, grade=None, age=None, gender=None, marital_status=None, job=None, sheba_number=None, credit_score=None, user_type=None, invited_friend_mobile=None, last_login_datetime=None, national_id=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if full_name:
            update_string += f'full_name = %(full_name)s,'
        if mobile:
            update_string += f'mobile=%(mobile)s,'
        if sheba_number:
            update_string += f'sheba_number=%(sheba_number)s,'
        if credit_score:
            update_string += f'credit_score=%(credit_score)s,'
        if user_type:
            update_string += f'user_type=%(user_type)s,'
        if invited_friend_mobile:
            update_string += f'invited_friend_mobile=%(invited_friend_mobile)s,'
        if last_login_datetime:
            update_string += f'last_login_datetime=%(last_login_datetime)s,'
        if national_id:
            update_string += f'national_id=%(national_id)s,'
        if grade:
            update_string += f'grade=%(grade)s,'
        if age:
            update_string += f'age=%(age)s,'
        if gender:
            update_string += f'gender=%(gender)s,'
        if marital_status:
            update_string += f'marital_status=%(marital_status)s,'
        if job:
            update_string += f'job=%(job)s,'
        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_users SET {update_string} WHERE id='{id}'"
        update_query_string = {
            'full_name': full_name,
            'mobile': mobile,
            'sheba_number': sheba_number,
            'credit_score': credit_score,
            'user_type': user_type,
            'invited_friend_mobile': invited_friend_mobile,
            'last_login_datetime': last_login_datetime,
            'national_id': national_id,
            'grade': grade,
            'age': age,
            'gender': gender,
            'marital_status': marital_status,
            'job': job,
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
        query = 'DELETE FROM tbl_users WHERE id = "%(id)s"'
        cursor.execute(query, {'id': user_id})
        cnx.commit()
        cnx.close()
        return True

    class Types(enum.Enum):
        blocked_user = enum.auto()
        new_user = enum.auto()
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
