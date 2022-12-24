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
    def get_all_quizzes_by_ids(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        # query = "SELECT tbl_items.course_id, tbl_items.id, tbl_quizzes.* FROM tbl_items INNER JOIN tbl_quizzes ON tbl_items.id = tbl_quizzes.item_id WHERE (tbl_quizzes.item_id='%(item_id)s' AND tbl_items.course_id='%(course_id)s')"
        query = ("SELECT * FROM tbl_quizzes WHERE item_id=%(item_id)s")
        cursor.execute(query, {'item_id': item_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def insert_new_quiz(item_id, title, jalali_start_datetime, jalali_end_datetime, description, question_count, duration, attendance_max, quiz_type):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_quiz = ("INSERT INTO `tbl_quizzes` (`item_id`, `title`, `jalali_start_datetime`, `jalali_end_datetime`, `description`, `question_count`, `duration`, `attendance_max`, `quiz_type`) VALUES" +
                    "( %(item_id)s, %(title)s, %(jalali_start_datetime)s, %(jalali_end_datetime)s, %(description)s, %(question_count)s, %(duration)s, %(attendance_max)s, %(quiz_type)s)")
        data_quiz = {
            'item_id': item_id,
            'title': title,
            'jalali_start_datetime': jalali_start_datetime,
            'jalali_end_datetime': jalali_end_datetime,
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
    def update_quiz(id, title=None, jalali_start_datetime=None, jalali_end_datetime=None, description=None, question_count=None, duration=None, attendance_max=None, quiz_type=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if title:
            update_string += f'title = %(title)s,'
        if jalali_start_datetime:
            update_string += f'jalali_start_datetime=%(jalali_start_datetime)s,'
        if jalali_end_datetime:
            update_string += f'jalali_end_datetime=%(jalali_end_datetime)s,'
        if description:
            update_string += f'description=%(description)s,'
        if question_count:
            update_string += f'question_count=%(question_count)s,'
        if duration:
            update_string += f'duration=%(duration)s,'
        if attendance_max:
            update_string += f'attendance_max=%(attendance_max)s,'
        if quiz_type:
            update_string += f"quiz_type=%(quiz_type)s"
        update_string = update_string.rstrip(',')
        add_quiz = f"UPDATE tbl_quizzes SET {update_string} WHERE id='{id}'"
        data_quiz = {
            'title': title,
            'jalali_start_datetime': jalali_start_datetime,
            'jalali_end_datetime': jalali_end_datetime,
            'description': description,
            'question_count': question_count,
            'duration': duration,
            'attendance_max': attendance_max,
            'quiz_type': quiz_type,
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
        # query = "DELETE q.* FROM tbl_quizzes q INNER JOIN tbl_items i ON q.item_id = i.id WHERE (q.id='%(quiz_id)s' AND q.item_id='%(item_id)s' AND i.course_id = '%(course_id)s')"
        query = "DELETE FROM tbl_quizzes WHERE id = %(quiz_id)s"
        cursor.execute(query, {'quiz_id': quiz_id})
        cnx.commit()
        cnx.close()
        return True


def quizzes_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Quizzes.insert_new_quiz(
        f'title{i}', f'code{i}', f'unit_fa{i}', f'image_path{i}', f'description{i}', i, 0, f'{i*11}', i, i)
    update = Quizzes.update_quiz(last_id, title=f'Updated_title{i}')
    last_quiz = Quizzes.get_quiz_by_id(last_id)
    print(last_quiz)
    print('-' * 80)
    all_quizzes = Quizzes.get_all_quizzes()
    print(all_quizzes)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    quizzes_orm_functions_test()
    print('Everything is alright!')
