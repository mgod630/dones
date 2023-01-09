from flask import current_app as app
import mysql.connector.pooling
import uuid
import enum

connection_pool = None

class Notifications:
    @staticmethod
    def get_all_notifications():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_notifications")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_notification_by_id_and_user_id(user_id, notification_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notifications WHERE (receiver_id=%(user_id)s AND id=%(id)s)"
        cursor.execute(query, {'id': notification_id, 'user_id': user_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_all_notifications_by_receiver_id(receiver_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notifications WHERE receiver_id=%(receiver_id)s"
        cursor.execute(query, {'receiver_id': receiver_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_all_notifications_with_users():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT t.*, u.full_name, u.mobile FROM tbl_notifications t INNER JOIN tbl_users u ON u.id = t.user_id"
        cursor.execute(query)
        row = cursor.fetchall()
        cnx.close()
        return row
    
    @staticmethod
    def get_unread_notifications_count_by_receiver_id(receiver_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        is_read = Notifications.Read_status.unread.value
        query = 'SELECT COUNT(receiver_id) FROM tbl_comments WHERE (receiver_id=%(receiver_id)s AND is_read=%(is_read)s);'
        cursor.execute(query, {'receiver_id': receiver_id, 'is_read': is_read})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def insert_new_notification(receiver_id, notification_text, unix_datetime, is_read):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_notification = ("INSERT INTO `tbl_notifications` (`receiver_id`, `notification_text`, `unix_datetime`, `is_read`) VALUES" +
                           "(%(receiver_id)s, %(notification_text)s, %(unix_datetime)s, %(is_read)s)")
        data_notification = {
            'receiver_id': receiver_id,
            'notification_text': notification_text,
            'unix_datetime': unix_datetime,
            'is_read': is_read
        }
        cursor.execute(add_notification, data_notification)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_notification(id, receiver_id=None, notification_text=None, unix_datetime=None, is_read=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if receiver_id:
            update_string += f'receiver_id = %(receiver_id)s,'
        if notification_text:
            update_string += f'notification_text=%(notification_text)s,'
        if unix_datetime:
            update_string += f'unix_datetime=%(unix_datetime)s,'
        if is_read:
            update_string += f'is_read=%(is_read)s'
        update_string = update_string.rstrip(',')
        add_notification = f"UPDATE tbl_notifications SET {update_string} WHERE id='{id}'"
        data_notification = {
            'receiver_id': receiver_id,
            'notification_text': notification_text,
            'unix_datetime': unix_datetime,
            'is_read': is_read
        }
        cursor.execute(add_notification, data_notification)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_notification_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_notifications WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        return True

    class Read_status(enum.Enum):
        unread = enum.auto()
        read = enum.auto()

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)

