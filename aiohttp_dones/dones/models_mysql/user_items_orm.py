import enum
from flask import current_app as app
import mysql.connector.pooling
from routes import common
from models_mysql import user_courses_orm, courses_orm

connection_pool = None


class User_items:
    @staticmethod
    def get_all_user_items():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_user_items")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_all_user_items_by_user_id(user_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_items WHERE (user_id=%(user_id)s)"
        cursor.execute(query, {'user_id': user_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_user_items_by_ids(user_id, course_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT ui.*, i.course_id, i.id FROM tbl_user_items ui INNER JOIN tbl_items i ON i.id = ui.item_id WHERE (ui.user_id=%(user_id)s AND i.course_id=%(course_id)s) ")
        cursor.execute(query, {'user_id': user_id, 'course_id': course_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_user_item_by_ids(user_id, item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_items WHERE (item_id=%(item_id)s AND user_id=%(user_id)s)"
        cursor.execute(query, {'user_id': user_id, 'item_id': item_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_last_rowid():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute('SELECT id FROM tbl_user_items ORDER BY id DESC LIMIT 1;') 
        last_rowid = cursor.fetchone()
        cnx.commit()
        cnx.close()
        return last_rowid

    @staticmethod
    def insert_new_user_item(user_id, item_id, unix_datetime):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user = ("INSERT INTO `tbl_user_items` (`user_id`, `unix_datetime`, `item_id`) VALUES" +
                    "( %(user_id)s, %(unix_datetime)s, %(item_id)s)")
        data_user = {
            'user_id': user_id,
            'unix_datetime': unix_datetime,
            'item_id': item_id,
        }
        cursor.execute(add_user, data_user)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user_item(row_id, item_id=None, unix_datetime=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if unix_datetime:
            update_string += f'unix_datetime=%(unix_datetime)s,'
        if item_id:
            update_string += f'item_id=%(item_id)s,'

        update_string = update_string.rstrip(',')
        add_user = f"UPDATE tbl_user_items SET {update_string} WHERE id='{row_id}'"
        update_query_string = {
            'item_id': item_id,
            'unix_datetime': unix_datetime,
        }
        cursor.execute(add_user, update_query_string)
        cnx.commit()
        cnx.close()
        return True

    # delete
    @staticmethod
    def delete_all_user_items():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_user_items')
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
        query = 'DELETE FROM tbl_user_items WHERE id = %(id)s'
        cursor.execute(query, {'id': user_id})
        cnx.commit()
        cnx.close()
        return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
