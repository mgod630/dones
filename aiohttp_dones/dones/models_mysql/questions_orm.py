from flask import current_app as app
import mysql.connector.pooling

connection_pool = None


class Questions:
    @staticmethod
    def get_all_questions():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_questions ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_all_questions_by_id_quiz_id(quiz_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_questions WHERE quiz_id=%(quiz_id)s")
        cursor.execute(query, {'quiz_id': quiz_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_question_by_id(question_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_questions WHERE id=%(id)s"
        cursor.execute(query, {'id': question_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_question(quiz_id, question_text, options, answer_number, answer_description):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_question = ("INSERT INTO `tbl_questions` (`quiz_id`, `question_text`, `options`, `answer_number`, `answer_description`) VALUES" +
                        "( %(quiz_id)s, %(question_text)s, %(options)s, %(answer_number)s, %(answer_description)s)")
        data_question = {
            'quiz_id': quiz_id,
            'question_text': question_text,
            'options': options,
            'answer_number': answer_number,
            'answer_description': answer_description
        }
        cursor.execute(add_question, data_question)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_question(id, question_text=None, options=None, answer_number=None, answer_description=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if question_text:
            update_string += f'question_text = %(question_text)s,'
        if options:
            update_string += f'options=%(options)s,'
        if answer_number:
            update_string += f'answer_number=%(answer_number)s,'
        if answer_description:
            update_string += f'answer_description=%(answer_description)s,'
        update_string = update_string.rstrip(',')
        add_question = f"UPDATE tbl_questions SET {update_string} WHERE id='{id}'"
        data_question = {
            'question_text': question_text,
            'options': options,
            'answer_number': answer_number,
            'answer_description': answer_description
        }
        cursor.execute(add_question, data_question)
        cnx.commit()
        cnx.close()
        return True

    # delete
    @staticmethod
    def delete_all_questions():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_questions')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_question_by_id(question_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_questions WHERE id = %(question_id)s"
        cursor.execute(query, {'question_id': question_id})
        cnx.commit()
        cnx.close()
        return True


def questions_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Questions.insert_new_question(
        f'title{i}', f'code{i}', f'unit_fa{i}', f'image_path{i}', f'description{i}', i, 0, f'{i*11}', i, i)
    update = Questions.update_question(last_id, title=f'Updated_title{i}')
    last_question = Questions.get_question_by_id(last_id)
    print(last_question)
    print('-' * 80)
    all_questions = Questions.get_all_questions()
    print(all_questions)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    questions_orm_functions_test()
    print('Everything is alright!')
