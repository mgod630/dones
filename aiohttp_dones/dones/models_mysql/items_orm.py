from flask import current_app as app
import mysql.connector.pooling

connection_pool = None

class Items:
    @staticmethod
    def get_all_items():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_items ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_item_by_id(item_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_items WHERE id=%(id)s"
        cursor.execute(query, {'id': item_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_all_items_by_course_id(course_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_items WHERE course_id=%(course_id)s")
        cursor.execute(query, {'course_id': course_id})
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def insert_new_item(course_id=0, title='empty', unix_start_datetime=0, unix_end_datetime=0, description='empty'):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_item = ("INSERT INTO `tbl_items` (`course_id`, `title`, `unix_start_datetime`, `unix_end_datetime`, `description`) VALUES" +
                    "( %(course_id)s, %(title)s, %(unix_start_datetime)s, %(unix_end_datetime)s, %(description)s)")
        data_item = {
            'course_id': course_id,
            'title': title,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'description': description
        }
        cursor.execute(add_item, data_item)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_item(id, title='empty', unix_start_datetime=0, unix_end_datetime=0, description='empty'):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if title:
            update_string += f'title = %(title)s,'
        if unix_start_datetime:
            update_string += f'unix_start_datetime=%(unix_start_datetime)s,'
        if unix_end_datetime:
            update_string += f'unix_end_datetime=%(unix_end_datetime)s,'
        if description:
            update_string += f'description=%(description)s'
        update_string = update_string.rstrip(',')
        add_item = f"UPDATE tbl_items SET {update_string} WHERE id='{id}'"
        data_item = {
            'title': title,
            'unix_start_datetime': unix_start_datetime,
            'unix_end_datetime': unix_end_datetime,
            'description': description
        }
        cursor.execute(add_item, data_item)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_item_by_id(id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_items WHERE id=%(id)s"
        cursor.execute(query, {'id': id})
        cnx.commit()
        cnx.close()
        return True


def items_orm_functions_test():
    # import random
    # i = random.randint(1, 1000)
    # last_id = Items.insert_new_item(
    #     f'title{i}', f'description{i}')
    # update = Items.update_item(last_id, title=f'Updated_title{i}')
    # last_item = Items.get_item_by_id(last_id)
    Items.insert_new_item(course_id=13, title='جلسه 1',description='deieei')
    all_items = Items.get_all_items()
    
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='full_stack', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    items_orm_functions_test()
    print('Everything is alright!')
