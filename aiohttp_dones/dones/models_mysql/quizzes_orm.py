from flask import current_app as app
import mysql.connector.pooling
from models_mysql import items_orm

connection_pool = None

class Quizzes:
    @staticmethod
    def get_all_quizzes():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_quizzes ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_quiz_by_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_quizzes WHERE id=%(id)s"
        cursor.execute(query, {'id': quiz_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_all_quizzes_by_item_id(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_quizzes WHERE item_id=%(item_id)s")
        cursor.execute(query, {'item_id': item_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_quizzes_with_questions(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT qz.*, qs.question_text, qs.options, qs.answer_number, qs.answer_description FROM tbl_quizzes qz INNER JOIN tbl_questions qs ON qs.quiz_id = qz.id WHERE qz.item_id=%(item_id)s")
        cursor.execute(query, {'item_id': item_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def insert_new_quiz(item_id, title, unix_start_datetime, unix_end_datetime, description='empty', question_count=0, duration=1, attendance_max=1, quiz_type=1):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        if question_count == '': question_count = 0
        else: question_count = int(question_count)
        if duration == '': duration = 1
        else: duration = int(duration)
        if attendance_max == '' : attendance_max = 1
        else: attendance_max = int(attendance_max)
        add_quiz = ("INSERT INTO `tbl_quizzes` (`item_id`, `title`, `unix_start_datetime`, `unix_end_datetime`, `description`, `question_count`, `duration`, `attendance_max`, `quiz_type`) VALUES" +
                    "( %(item_id)s, %(title)s, %(unix_start_datetime)s, %(unix_end_datetime)s, %(description)s, %(question_count)s, %(duration)s, %(attendance_max)s, %(quiz_type)s)")
        data_quiz = {
            'item_id': item_id,
            'title': title,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'description': description,
            'question_count': question_count,
            'duration': duration,
            'attendance_max': attendance_max,
            'quiz_type': quiz_type,
        }
        cursor.execute(add_quiz, data_quiz)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_quiz(id, title=None, unix_start_datetime=None, unix_end_datetime=None, description=None, question_count=None, duration=None, attendance_max=None, quiz_type=None, user_answers='empty'):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if title:
            update_string += f'title = %(title)s,'
        if unix_start_datetime:
            update_string += f'unix_start_datetime=%(unix_start_datetime)s,'
        if unix_end_datetime:
            update_string += f'unix_end_datetime=%(unix_end_datetime)s,'
        if description:
            update_string += f'description=%(description)s,'
        if question_count:
            update_string += f'question_count=%(question_count)s,'
        if duration:
            update_string += f'duration=%(duration)s,'
        if attendance_max:
            update_string += f'attendance_max=%(attendance_max)s,'
        if quiz_type:
            update_string += f"quiz_type=%(quiz_type)s,"
        if user_answers:
            update_string += f"user_answers=%(user_answers)s"
        update_string = update_string.rstrip(',')
        add_quiz = f"UPDATE tbl_quizzes SET {update_string} WHERE id='{id}'"
        data_quiz = {
            'title': title,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'description': description,
            'question_count': question_count,
            'duration': duration,
            'attendance_max': attendance_max,
            'quiz_type': quiz_type,
            'user_answers': user_answers
        }
        cursor.execute(add_quiz, data_quiz)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_quiz_by_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_quizzes WHERE id = %(quiz_id)s"
        cursor.execute(query, {'quiz_id': quiz_id})
        cnx.commit()
        cnx.close()
        return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
