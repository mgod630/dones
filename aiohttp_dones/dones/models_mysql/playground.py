import mysql.connector.pooling

connection_pool = None


class User_types:
    @staticmethod
    def get_all_user_types():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_user_types ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_user_type_by_id(user_type_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_types WHERE id='%(id)s'"
        cursor.execute(query, {'id': user_type_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_user_type_by_description(description):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_user_types WHERE description=%(description)s"
        cursor.execute(query, {'description': description})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_user_type(title, description):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_user_type = ("INSERT INTO `tbl_user_types` (`title`, `description`) VALUES" +
                         "( %(title)s, %(description)s)")
        data_user_type = {
            'title': title,
            'description': description,
        }
        cursor.execute(add_user_type, data_user_type)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_user_type(id, title=None, description=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if title:
            update_string += f'title = %(title)s,'
        if description:
            update_string += f'description=%(description)s,'
        update_string = update_string.rstrip(',')
        add_user_type = f"UPDATE tbl_user_types SET {update_string} WHERE id='{id}'"
        data_user_type = {
            'title': title,
            'description': description,
        }
        cursor.execute(add_user_type, data_user_type)
        cnx.commit()
        cnx.close()
        return True


def user_types_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = User_types.insert_new_user_type(f'title{i}', f'description{i}')
    update = User_types.update_user_type(last_id, title=f'Updated_title{i}')
    last_user_type = User_types.get_user_type_by_id(last_id)
    print(last_user_type)
    print('-' * 80)
    all_user_types = User_types.get_all_user_types()
    print(all_user_types)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='full_stack', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    user_types_orm_functions_test()
    print('Everything is alright!')
