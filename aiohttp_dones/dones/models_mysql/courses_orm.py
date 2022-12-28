from flask import current_app as app
import mysql.connector.pooling

connection_pool = None

class Courses:
    @staticmethod
    def get_all_courses():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_courses ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_course_by_id(course_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_courses WHERE id=%(id)s"
        cursor.execute(query, {'id': course_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_course(welcome_text, body_html, title, institute, unix_start_datetime, unix_end_datetime, price, logo_path, image_path, description, video_path):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_course = ("INSERT INTO `tbl_courses` (`welcome_text`, `body_html`, `title`, `institute`, `unix_start_datetime`, `unix_end_datetime`, `price`, `logo_path`, `image_path`, `description`, `video_path`) VALUES" +
                      "( %(welcome_text)s, %(body_html)s, %(title)s, %(institute)s, %(unix_start_datetime)s, %(unix_end_datetime)s, %(price)s, %(logo_path)s, %(image_path)s, %(description)s, %(video_path)s)")
        data_course = {
            'welcome_text': welcome_text,
            'body_html': body_html,
            'title': title,
            'institute': institute,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'price': price,
            'logo_path': logo_path,
            'image_path': image_path,
            'description': description,
            'video_path': video_path,
        }
        cursor.execute(add_course, data_course)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_course(id, welcome_text=None, body_html=None, title=None, institute=None, unix_start_datetime=None, unix_end_datetime=None, price=None, logo_path=None, image_path=None, description=None, video_path=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if welcome_text:
            update_string += f'welcome_text=%(welcome_text)s,'
        if body_html:
            update_string += f'body_html=%(body_html)s,'
        if title:
            update_string += f'title = %(title)s,'
        if institute:
            update_string += f'institute=%(institute)s,'
        if unix_start_datetime:
            update_string += f'unix_start_datetime=%(unix_start_datetime)s,'
        if unix_end_datetime:
            update_string += f'unix_end_datetime=%(unix_end_datetime)s,'
        if price:
            update_string += f'price=%(price)s,'
        if logo_path:
            update_string += f'logo_path=%(logo_path)s,'
        if image_path:
            update_string += f'image_path=%(image_path)s,'
        if description:
            update_string += f'description=%(description)s,'
        if video_path:
            update_string += f'video_path=%(video_path)s,'
        update_string = update_string.rstrip(',')
        add_course = f"UPDATE tbl_courses SET {update_string} WHERE id='{id}'"
        data_course = {
            'welcome_text': welcome_text,
            'body_html': body_html,
            'title': title,
            'institute': institute,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'price': price,
            'logo_path': logo_path,
            'image_path': image_path,
            'description': description,
            'video_path': video_path,
        }
        cursor.execute(add_course, data_course)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_courses():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_courses')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_course_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_courses WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        return True

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    
