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
    def get_notification_by_id(notification_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        notification_id_int = int(notification_id)
        query = "SELECT * FROM tbl_notifications WHERE id='%(id)s'"
        cursor.execute(query, {'id': notification_id_int})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_notification(welcome_text, body_html, free_items_count, notification_result, title, institute, jalali_start_datetime, jalali_end_datetime, price, logo_path, image_path, description, video_path):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_notification = ("INSERT INTO `tbl_notifications` (`welcome_text`, `body_html`, `free_items_count`, `notification_result`, `title`, `institute`, `jalali_start_datetime`, `jalali_end_datetime`, `price`, `logo_path`, `image_path`, `description`, `video_path`) VALUES" +
                      "( %(welcome_text)s, %(body_html)s, %(free_items_count)s, %(notification_result)s, %(title)s, %(institute)s, %(jalali_start_datetime)s, %(jalali_end_datetime)s, %(price)s, %(logo_path)s, %(image_path)s, %(description)s, %(video_path)s)")
        data_notification = {
            'welcome_text': welcome_text,
            'body_html': body_html,
            'free_items_count': free_items_count,
            'notification_result': notification_result,
            'title': title,
            'institute': institute,
            'jalali_start_datetime': jalali_start_datetime,
            'jalali_end_datetime': jalali_end_datetime,
            'price': price,
            'logo_path': logo_path,
            'image_path': image_path,
            'description': description,
            'video_path': video_path,
        }
        cursor.execute(add_notification, data_notification)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_notification(id, welcome_text=None, body_html=None, free_items_count=None, notification_result=None, title=None, institute=None, jalali_start_datetime=None, jalali_end_datetime=None, price=None, logo_path=None, image_path=None, description=None, video_path=None):
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
        if free_items_count:
            update_string += f'free_items_count=%(free_items_count)s,'
        if notification_result:
            update_string += f'notification_result=%(notification_result)s,'
        if title:
            update_string += f'title = %(title)s,'
        if institute:
            update_string += f'institute=%(institute)s,'
        if jalali_start_datetime:
            update_string += f'jalali_start_datetime=%(jalali_start_datetime)s,'
        if jalali_end_datetime:
            update_string += f'jalali_end_datetime=%(jalali_end_datetime)s,'
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
        add_notification = f"UPDATE tbl_notifications SET {update_string} WHERE id='{id}'"
        data_notification = {
            'welcome_text': welcome_text,
            'body_html': body_html,
            'free_items_count': free_items_count,
            'notification_result': notification_result,
            'title': title,
            'institute': institute,
            'jalali_start_datetime': jalali_start_datetime,
            'jalali_end_datetime': jalali_end_datetime,
            'price': price,
            'logo_path': logo_path,
            'image_path': image_path,
            'description': description,
            'video_path': video_path,
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
        query = "DELETE FROM tbl_notifications WHERE id='%(id)s'"
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
