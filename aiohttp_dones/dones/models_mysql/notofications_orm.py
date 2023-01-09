import enum
import time
from datetime import datetime
import mysql.connector.pooling
from flask import current_app as app

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
    def get_notification_by_id(notification_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notifications WHERE id=%(id)s"
        cursor.execute(query, {'id': notification_id})
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
        row = cursor.fetchone()
        cnx.close()
        return row
    
    @staticmethod
    def get_notifications_count_by_receiver_id(receiver_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = 'SELECT COUNT(receiver_id) FROM tbl_comments WHERE (receiver_id=%(receiver_id)s AND is_read=0);'
        cursor.execute(query, {'receiver_id': receiver_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_notification(receiver_id, notification_text, unix_datetime, is_read=0):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_notification = ("INSERT INTO `tbl_notifications` (`receiver_id`, `notification_text`, `unix_datetime`, `is_read`) VALUES" +
                           "( %(receiver_id)s, %(notification_text)s, %(unix_datetime)s, %(is_read)s)")
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

        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if is_read:
            update_string += f'is_read=%(is_read)s,'
        if notification_type:
            update_string += f'notification_type=%(notification_type)s,'
        if status:
            update_string += f'status=%(status)s,'
        if description:
            update_string += f'description=%(description)s,'
        if ipg_invoice_number:
            update_string += f'ipg_invoice_number=%(ipg_invoice_number)s'
        update_string = update_string.rstrip(',')
        add_notification = f"UPDATE tbl_notifications SET {update_string} WHERE ipg_ref_id='{ipg_ref_id}'"
        data_notification = {
            'is_read': is_read,
            'notification_type': notification_type,
            'status': status,
            'description': description,
            'ipg_invoice_number': ipg_invoice_number
        }
        cursor.execute(add_notification, data_notification)
        cnx.commit()
        cnx.close()
        return True

    class Status(enum.Enum):
        Unknown = enum.auto()
        successful = enum.auto()
        failed = enum.auto()
        pending = enum.auto()
        expired = enum.auto()
        queued = enum.auto()
        canceling = enum.auto()
        canceled = enum.auto()

    class Types(enum.Enum):
        ipg_cash_deposit = enum.auto()
        admin_cash_deposit = enum.auto()
        gift_cash_deposit = enum.auto()
        buy_token = enum.auto()



if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    print('Everything is alright!')
