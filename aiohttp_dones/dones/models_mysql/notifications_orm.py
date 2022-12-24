from flask import current_app as app
import mysql.connector.pooling
import uuid

connection_pool = None

class Notifications:
    @staticmethod
    def get_all_notifications():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_notifications ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_notifications_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notifications WHERE section_id=%(section_id)s"
        cursor.execute(query, {'section_id': section_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_notification_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notifications WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_notification(section_id, jalali_date, notification_type, notification_text):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_notification = ("INSERT INTO `tbl_notifications` (`section_id`, `jalali_date`, `notification_type`, `notification_text`) VALUES" +
                      "( %(section_id)s, %(jalali_date)s, %(notification_type)s, %(notification_text)s)")
        data_notification = {
            'section_id': section_id,
            'jalali_date': jalali_date,
            'notification_type': notification_type,
            'notification_text': notification_text,
        }
        cursor.execute(add_notification, data_notification)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_notification(id, section_id, jalali_date, notification_type, notification_text):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if section_id:
            update_string += f'section_id=%(section_id)s,'
        if jalali_date:
            update_string += f'jalali_date=%(jalali_date)s,'
        if notification_type:
            update_string += f'notification_type=%(notification_type)s,'
        if notification_text:
            update_string += f'notification_text=%(notification_text)s,'
        update_string = update_string.rstrip(',')
        add_notification = f"UPDATE tbl_notifications SET {update_string} WHERE id='{id}'"
        data_notification = {
            'section_id': section_id,
            'jalali_date': jalali_date,
            'notification_type': notification_type,
            'notification_text': notification_text,
        }
        cursor.execute(add_notification, data_notification)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_notifications():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_notifications')
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
        print('deleted')
        return True


def notifications_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Notifications.insert_new_notification(
        f'title{i}', f'code{i}', f'unit_fa{i}', f'image_path{i}', f'description{i}', i, 0, f'{i*11}', i, i)
    update = Notifications.update_notification(last_id, title=f'Updated_title{i}')
    last_notification = Notifications.get_notification_by_id(last_id)
    print(last_notification)
    print('-' * 80)
    all_notifications = Notifications.get_all_notifications()
    print(all_notifications)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    notifications_orm_functions_test()
    print('Everything is alright!')
