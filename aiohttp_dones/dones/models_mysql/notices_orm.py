from flask import current_app as app
import mysql.connector.pooling

connection_pool = None

class Notices:
    @staticmethod
    def get_all_notices():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_notices ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_notices_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notices WHERE section_id=%(section_id)s"
        cursor.execute(query, {'section_id': section_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_notice_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_notices WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_notice(section_id, jalali_date, notice_type, notice_text):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_notice = ("INSERT INTO `tbl_notices` (`section_id`, `jalali_date`, `notice_type`, `notice_text`) VALUES" +
                      "( %(section_id)s, %(jalali_date)s, %(notice_type)s, %(notice_text)s)")
        data_notice = {
            'section_id': section_id,
            'jalali_date': jalali_date,
            'notice_type': notice_type,
            'notice_text': notice_text,
        }
        cursor.execute(add_notice, data_notice)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_notice(id, section_id, jalali_date, notice_type, notice_text):
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
        if notice_type:
            update_string += f'notice_type=%(notice_type)s,'
        if notice_text:
            update_string += f'notice_text=%(notice_text)s,'
        update_string = update_string.rstrip(',')
        add_notice = f"UPDATE tbl_notices SET {update_string} WHERE id='{id}'"
        data_notice = {
            'section_id': section_id,
            'jalali_date': jalali_date,
            'notice_type': notice_type,
            'notice_text': notice_text,
        }
        cursor.execute(add_notice, data_notice)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_notices():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tbl_notices')
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_notice_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_notices WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        print('deleted')
        return True

if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
