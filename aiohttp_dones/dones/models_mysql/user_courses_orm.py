import enum
from flask import current_app as app
import mysql.connector.pooling
from routes import common
from models_mysql import items_orm, quizzes_orm, courses_orm

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
    def get_all_registered_users_by_quiz_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT tbl_user_courses.*, tbl_users.* FROM tbl_user_courses INNER JOIN tbl_users ON tbl_user_courses.user_id = tbl_users.id WHERE quiz_id=%(quiz_id)s")
        data = { 
            'quiz_id':quiz_id
        }
        cursor.execute(query, data)
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
        query = "SELECT * FROM tbl_user_courses WHERE (user_id=%(user_id)s AND quiz_id IS NULL)"
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
    def get_all_user_results_by_ids(user_id, quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT user_answers FROM tbl_user_courses WHERE (user_id=%(user_id)s AND quiz_id=%(quiz_id)s)"
        cursor.execute(query, {'user_id': user_id, 'quiz_id': quiz_id})
        row = cursor.fetchall()
        cnx.close()
        return row
        
    @staticmethod
    def get_user_courses_by_item_id(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE item_id=%(item_id)s"
        cursor.execute(query, {'item_id': item_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_user_quizzes_by_item_id(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT tbl_user_courses.*,tbl_quizzes.* FROM tbl_user_courses INNER JOIN tbl_quizzes ON tbl_quizzes.item_id = tbl_user_courses.item_id WHERE (tbl_user_courses.item_id=%(item_id)s AND tbl_user_courses.quiz_id IS NOT NULL)"
        cursor.execute(query, {'item_id': item_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_user_quiz_by_quiz_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_courses WHERE quiz_id=%(quiz_id)s"
        cursor.execute(query, {'quiz_id': quiz_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user_course(user_id, jalali_date=None, jalali_time=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_user_courses` (`user_id`, `jalali_date`, `jalali_time`) VALUES" +
                    "( %(user_id)s, %(jalali_date)s, %(jalali_time)s)")
        data_user = {
            'user_id': user_id,
            'jalali_date': jalali_date,
            'jalali_time': jalali_time,
        }
        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user_course(row_id, quiz_id=None, item_id=None, user_answers=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if item_id : 
          item = items_orm.Items.get_item_by_id(item_id)
          course = courses_orm.Courses.get_course_by_id(item['course_id'])
          course_id = item['course_id']
          item_title = f"{item['title']} درس {course['title']}"
          update_string += f'item_id = %(item_id)s,'
          update_string += f'course_id = %(course_id)s,'
          update_string += f'title = %(title)s,'
        
        if quiz_id:
          print('sql' + quiz_id)
          quiz = quizzes_orm.Quizzes.get_quiz_by_id(quiz_id)
          item_id = quiz['item_id'] 
          item = items_orm.Items.get_item_by_id(item_id)
          course = courses_orm.Courses.get_course_by_id(item['course_id'])
          course_id = item['course_id']
          item_title = f"آزمون {quiz['title']}"
          update_string += f'item_id = %(item_id)s,'
          update_string += f'course_id = %(course_id)s,'
          update_string += f'quiz_id=%(quiz_id)s,'
          update_string += f'title = %(title)s,'
          update_string += f'user_answers = %(user_answers)s'
          
        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_user_courses SET {update_string} WHERE id='{row_id}'"
        update_query_string = {
            'item_id':item_id,
            'course_id':course_id,
            'quiz_id': quiz_id,
            'title': item_title,
            'user_answers': user_answers
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
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
