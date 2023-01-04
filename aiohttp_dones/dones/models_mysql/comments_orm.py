from flask import current_app as app
import mysql.connector.pooling
import uuid

connection_pool = None


class Comments:
    @staticmethod
    def get_all_comments():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_comments ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_comment_by_id(comment_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_comments WHERE id=%(id)s"
        cursor.execute(query, {'id': comment_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_comments_id_by_reply_to_comment_id(reply_to_comment_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT id FROM tbl_comments WHERE reply_to_comment_id=%(reply_to_comment_id)s"
        cursor.execute(query, {'reply_to_comment_id': reply_to_comment_id})
        row = cursor.fetchall()
        cnx.close()
        return row

    @staticmethod
    def get_comments_by_section_id(section_id, comments_count_per_page=20, reversed_ordering=False):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        if reversed_ordering == True:
            query = "SELECT id FROM tbl_comments WHERE section_id=%(section_id)s ORDER BY id DESC;"
            cursor.execute(query, {'section_id': section_id})
            comments_ids = cursor.fetchall()
            cnx.close()
        else:
            query = "SELECT id FROM tbl_comments WHERE section_id=%(section_id)s ORDER BY id ASC"
            cursor.execute(query, {'section_id': section_id})
            comments_ids = cursor.fetchall()
            cnx.close()
        all_comments = []
        if comments_ids and len(comments_ids) > 0:
            for comment_id in comments_ids:
                comment = Comments.get_comment_by_id(comment_id['id'])
                if comment and comment['reply_to_comment_id'] == -1:
                    all_comments.append(comment)                  
                    reply_comments_id = Comments.get_comments_id_by_reply_to_comment_id(comment['id'])
                    if reply_comments_id != []:
                        for reply_comment_id in reply_comments_id:
                            reply_comment = Comments.get_comment_by_id(reply_comment_id['id'])
                            if reply_comment:
                                # reply_comment['depth'] = 2
                                Comments.update_comment(id=reply_comment['id'], depth=2)
                                all_comments.append(reply_comment)
        return all_comments

    @staticmethod
    def insert_new_comment(comment_text, sender_name, sender_id, section_id, reply_to_comment_id=-1, depth=0):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_comment = ("INSERT INTO `tbl_comments` (`comment_text`, `sender_name`, `sender_id`, `section_id`, `depth`,`reply_to_comment_id`) VALUES" +
                       "( %(comment_text)s, %(sender_name)s, %(sender_id)s, %(section_id)s, %(depth)s, %(reply_to_comment_id)s)")
        data_comment = {
            'comment_text': comment_text,
            'sender_name': sender_name,
            'sender_id': sender_id,
            'section_id': section_id,
            'depth': depth,
            'reply_to_comment_id': reply_to_comment_id,
        }
         
        cursor.execute(add_comment, data_comment)
        new_comment_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return new_comment_id

    @staticmethod
    def update_comment(id, comment_text=None, sender_name=None, sender_id=None, section_id=None, reply_to_comment_id=None, depth=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if comment_text:
            update_string += f'comment_text=%(comment_text)s,'
        if sender_name:
            update_string += f'sender_name=%(sender_name)s,'
        if sender_id:
            update_string += f'sender_id=%(sender_id)s,'
        if section_id:
            update_string += f'section_id=%(section_id)s,'
        if depth:
            update_string += f'depth=%(depth)s,'
        if reply_to_comment_id:
            update_string += f'reply_to_comment_id = %(reply_to_comment_id)s,'
        update_string = update_string.rstrip(',')
        add_comment = f"UPDATE tbl_comments SET {update_string} WHERE id='{id}'"
        data_comment = {
            'comment_text': comment_text,
            'sender_name': sender_name,
            'sender_id': sender_id,
            'section_id': section_id,
            'depth': depth,
            'reply_to_comment_id': reply_to_comment_id
        }
        cursor.execute(add_comment, data_comment)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def get_comments_count_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = 'SELECT COUNT(section_id) FROM tbl_comments WHERE section_id=%(section_id)s;'
        cursor.execute(query, {'section_id': section_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def delete_a_comment_by_id(comment_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_comments WHERE section_id='%(id)s'"
        cursor.execute(query, {'id': comment_id})
        cnx.commit()
        cnx.close()
        return True



    @staticmethod
    def delete_all_comments_by_section_id(section_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_comments WHERE section_id='%(id)s'"
        cursor.execute(query, {'id': section_id})
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def delete_all_comments():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM tbl_comments"
        cursor.execute(query)
        cnx.commit()
        cnx.close()
        return True


def comments_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Comments.insert_new_comment(
        f'title{i}', f'code{i}', f'unit_fa{i}', f'image_path{i}', f'description{i}', i, 0, f'{i*11}', i, i)
    update = Comments.update_comment(last_id, title=f'Updated_title{i}')
    last_comment = Comments.get_comment_by_id(last_id)
    print(last_comment)
    print('-' * 80)
    all_comments = Comments.get_all_comments()
    print(all_comments)
    return True


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    comments_orm_functions_test()
    print('Everything is alright!')
