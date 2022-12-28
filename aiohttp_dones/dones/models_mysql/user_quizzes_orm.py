import enum
from flask import current_app as app
import mysql.connector.pooling
from routes import common
from models_mysql import items_orm, quizzes_orm, courses_orm

connection_pool = None

class User_quizzes:
    @staticmethod
    def get_all_user_quizzes():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_user_quizzes")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_all_user_quizzes_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_quizzes WHERE (user_id=%(user_id)s)"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_user_quizzes_by_ids(user_id, item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT uq.*, q.item_id, q.id FROM tbl_user_quizzes uq INNER JOIN tbl_quizzes q ON q.id = uq.quiz_id WHERE (uq.user_id=%(user_id)s AND q.item_id=%(item_id)s)")
        cursor.execute(query, {'user_id': user_id, 'item_id': item_id})
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
        query = "SELECT user_answers FROM tbl_user_quizzes WHERE (user_id=%(user_id)s AND quiz_id=%(quiz_id)s)"
        cursor.execute(query, {'user_id': user_id, 'quiz_id': quiz_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_registered_users_by_quiz_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT tbl_user_quizzes.*, tbl_users.*, tbl_quizzes.title FROM tbl_user_quizzes INNER JOIN tbl_users ON tbl_user_quizzes.user_id = tbl_users.id INNER JOIN tbl_quizzes ON tbl_quizzes.id = tbl_user_quizzes.quiz_id WHERE quiz_id=%(quiz_id)s")
        data = { 
            'quiz_id':quiz_id
        }
        cursor.execute(query, data)
        data = cursor.fetchall()
        cnx.close()
        return data
        
    @staticmethod
    def get_user_quiz_by_quiz_id(user_id, quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT uq.*, q.item_id, q.id, q.title FROM tbl_user_quizzes uq INNER JOIN tbl_quizzes q ON q.id = uq.quiz_id WHERE (uq.user_id=%(user_id)s AND uq.quiz_id=%(quiz_id)s)"
        cursor.execute(query, {'quiz_id': quiz_id, 'user_id': user_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user_quiz(user_id, quiz_id, unix_datetime, user_answers='empty'):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_user_quizzes` (`user_id`, `unix_datetime`, `quiz_id`, `user_answers`) VALUES" +
                    "( %(user_id)s, %(unix_datetime)s, %(quiz_id)s, %(user_answers)s)")
        data_user = {
            'user_id': user_id,
            'unix_datetime': unix_datetime,
            'quiz_id': quiz_id,
            'user_answers': user_answers
        }
        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user_quiz(row_id, quiz_id=None, unix_datetime=None, user_answers=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if unix_datetime:
            update_string += f'unix_datetime=%(unix_datetime)s,'
        if quiz_id:
            update_string += f'quiz_id=%(quiz_id)s,'
        if user_answers:
            update_string += f'user_answers=%(user_answers)s,'
          
        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_user_quizzes SET {update_string} WHERE id='{row_id}'"
        update_query_string = {
            'quiz_id':quiz_id,
            'user_answers':user_answers,
            'unix_datetime': unix_datetime,
        }
        cursor.execute(add_user, update_query_string)
        cnx.commit()
        cnx.close()
        return True

    # delete
    @staticmethod
    def delete_all_user_quizzes():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_user_quizzes')
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
        query = 'DELETE FROM tbl_user_quizzes WHERE id = %(id)s'
        cursor.execute(query, {'id': user_id})
        cnx.commit()
        cnx.close()
        return True

 
if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
