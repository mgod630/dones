from flask import current_app as app
import mysql.connector.pooling
import enum

connection_pool = None

class Flash_messages:
    @staticmethod
    def get_all_flash_messages():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_flash_messages ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_flash_messages_by_user_token(user_token):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_flash_messages WHERE user_token=%(user_token)s"
        cursor.execute(query, {'user_token': user_token})
        row = cursor.fetchall()
        cnx.close()
        return row

    # class Message_types(enum.Enum):
    #   info = enum.auto()
    #   success = enum.auto()
    #   danger = enum.auto()

    @staticmethod
    def insert_new_flash_message(user_token, message, message_type):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_flash_message = ("INSERT INTO `tbl_flash_messages` (`user_token`, `message`, `message_type`) VALUES" +
                      "( %(user_token)s, %(message)s, %(message_type)s)")
        data_flash_message = {
            'user_token': user_token,
            'message': message,
            'message_type': message_type,
        }
        cursor.execute(add_flash_message, data_flash_message)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def delete_all_flash_messages():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_flash_messages')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_flash_message_by_user_token(user_token):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_flash_messages WHERE user_token=%(user_token)s"
        cursor.execute(query, {'user_token': user_token})
        cnx.commit()
        cnx.close()
        print('deleted')
        return True

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
