
from flask import current_app as app
import mysql.connector.pooling

connection_pool = None

class User_courses:
    @staticmethod
    def get_all_user_courses():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_user_courses")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_user_courses_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE user_id=%(user_id)s"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_user_quizzes_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE (user_id=%(user_id)s)"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchall()
        cnx.close()
        return row
        
    @staticmethod
    def get_user_course_by_ids(user_id, course_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE (user_id=%(user_id)s AND course_id=%(course_id)s)"
        cursor.execute(query, {'user_id': user_id, 'course_id': course_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user_course(user_id, course_id, unix_datetime, price):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_user_courses` (`user_id`, `unix_datetime`, `course_id`, `price`) VALUES" +
                    "( %(user_id)s, %(unix_datetime)s, %(course_id)s, %(price)s)")
        data_user = {
            'user_id': user_id,
            'unix_datetime': unix_datetime,
            'course_id': course_id,
            'price': price,
        }
        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user_course(row_id, course_id=None, unix_datetime=None, price=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''

        if unix_datetime:
            update_string += f'unix_datetime=%(unix_datetime)s,'
        if price:
            update_string += f'price=%(price)s,'
        if course_id:
            update_string += f'course_id=%(course_id)s,'
          
        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_user_courses SET {update_string} WHERE id='{row_id}'"
        update_query_string = {
            'course_id':course_id,
            'price': price,
            'unix_datetime': unix_datetime,
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

 
if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='full_stack', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
