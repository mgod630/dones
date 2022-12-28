from flask import current_app as app
import mysql.connector.pooling

connection_pool = None

class Emails:
    @staticmethod
    def get_all_emails():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_emails ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_emails_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_emails WHERE section_id=%(section_id)s"
        cursor.execute(query, {'section_id': section_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_email_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_emails WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_email(email):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_email = ("INSERT INTO `tbl_emails` (`email`) VALUES" +
                      "( %(email)s)")
        data_email = {
            'email': email,
        }
        cursor.execute(add_email, data_email)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_email(id, email):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if email:
            update_string += f'email=%(email)s,'
        update_string = update_string.rstrip(',')
        add_email = f"UPDATE tbl_emails SET {update_string} WHERE id='{id}'"
        data_email = {
            'email': email,
        }
        cursor.execute(add_email, data_email)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_emails():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_emails')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_email_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_emails WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        return True

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
