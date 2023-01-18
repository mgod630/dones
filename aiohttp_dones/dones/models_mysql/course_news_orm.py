from flask import current_app as app
import mysql.connector.pooling
import uuid

connection_pool = None

class Courses_news:
    @staticmethod
    def get_all_courses_news():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_courses_news ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_courses_news_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_courses_news WHERE section_id=%(section_id)s"
        cursor.execute(query, {'section_id': section_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_course_news_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_courses_news WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_course_news(section_id, unix_datetime, course_news_text):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_course_news = ("INSERT INTO `tbl_courses_news` (`section_id`, `unix_datetime`, `course_news_text`) VALUES" +
                      "( %(section_id)s, %(unix_datetime)s, %(course_news_text)s)")
        data_course_news = {
            'section_id': section_id,
            'unix_datetime': unix_datetime,
            'course_news_text': course_news_text,
        }
        cursor.execute(add_course_news, data_course_news)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_course_news(id, section_id, unix_datetime, course_news_text):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if section_id:
            update_string += f'section_id=%(section_id)s,'
        if unix_datetime:
            update_string += f'unix_datetime=%(unix_datetime)s,'
        if course_news_text:
            update_string += f'course_news_text=%(course_news_text)s,'
        update_string = update_string.rstrip(',')
        add_course_news = f"UPDATE tbl_courses_news SET {update_string} WHERE id='{id}'"
        data_course_news = {
            'section_id': section_id,
            'unix_datetime': unix_datetime,
            'course_news_text': course_news_text,
        }
        cursor.execute(add_course_news, data_course_news)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_courses_news():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_courses_news')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_course_news_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_courses_news WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        return True

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='full_stack', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)

