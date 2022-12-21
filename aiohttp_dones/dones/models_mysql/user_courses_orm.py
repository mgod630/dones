import enum
from flask import current_app as app
import mysql.connector.pooling
from routes import common
from models_mysql import items_orm, quizzes_orm

connection_pool = None

class User_courses:
    @staticmethod
    def get_all_user_courses():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_user_courses ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_user_course_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE user_id=%(user_id)s"
        cursor.execute(query, {'user_id': user_id})
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
        query = "SELECT * FROM tbl_user_courses WHERE g_token=%(g_token)s"
        cursor.execute(query, {'g_token': g_token})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user_course(item_id, quiz_id=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        item_title = None
        if item_id : 
          item = items_orm.Items.get_item_by_id(item_id)
          item_title = item['title']
        elif quiz_id:
          quiz = quizzes_orm.Quizzes.get_quiz_by_id(quiz_id)
          quiz_title = quiz['title']
  
        add_user = ("INSERT INTO `tbl_user_courses` (`item_id`, `quiz_id`, `user_course_item`) VALUES" +
                    "( %(item_id)s, %(quiz_id)s, %(user_course_item)s)")
        data_user = {
            'item_id': item_id,
            'quiz_id': quiz_id,
            'user_course_item': item_title
        }
        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user(id, full_name=None, mobile=None, password=None, grade=None, age=None, gender=None, marital_status=None, job=None, sheba_number=None, credit_score=None, user_type=None, invited_friend_mobile=None, last_login_datetime=None, national_id=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        password = common.get_hashed_password(password)
        update_string = ''
        if full_name:
            update_string += f'full_name = %(full_name)s,'
        if mobile:
            update_string += f'mobile=%(mobile)s,'
        if password:
            update_string += f'password=%(password)s,'
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
        add_user = f"UPDATE tbl_user_courses SET {update_string} WHERE id='{id}'"
        update_query_string = {
            'full_name': full_name,
            'mobile': mobile,
            'password': password,
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
    def delete_all_user_courses():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_user_courses')
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
        query = 'DELETE FROM tbl_user_courses WHERE id = %(id)s'
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


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
