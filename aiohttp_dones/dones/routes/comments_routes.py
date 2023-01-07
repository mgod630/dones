from flask import redirect, render_template, request, url_for
from models_mysql import course_news_orm, comments_orm
from routes import common
import time
from tools import date_converter

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_info_<course_id>')
    def json_get_comments_and_courses_news_course_info(course_id):
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        comments_count_per_page = 20
        section_id = course_id
        course_id = f'course_info_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(
            course_id, comments_count_per_page=comments_count_per_page, reversed_ordering=True)
        if page_number != None:
            start = page_number * comments_count_per_page - \
                comments_count_per_page if page_number > 0 else 0
            end = start + comments_count_per_page
            a_page_section_comments = a_page_section_comments[start:end]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(
            course_id)
        pages_count = (comments_count[0] // comments_count_per_page) + 1
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(
            section_id)
        for comment in a_page_section_comments:
            comment['jalali_datetime'], time = date_converter.Date_converter.unix_timestamp_to_jalali(comment['unix_datetime']).split(' ')
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id, 'all_courses_news': all_courses_news}

    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_overview_<course_id>')
    def json_get_comments_course_overview(course_id):
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        comments_count_per_page = 20
        course_id = f'course_overview_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(
            course_id, comments_count_per_page=comments_count_per_page, reversed_ordering=True)
        start = page_number * comments_count_per_page - \
            comments_count_per_page if page_number > 0 else 0
        end = start + comments_count_per_page
        a_page_section_comments = a_page_section_comments[start:end]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(
            course_id)
        pages_count = (comments_count[0] // comments_count_per_page) + 1
        for comment in a_page_section_comments:
            comment['jalali_datetime'], time = date_converter.Date_converter.unix_timestamp_to_jalali(comment['unix_datetime']).split(' ')
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id}

    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_content_<item_id>')
    def json_get_comments_course_content(item_id):
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        comments_count_per_page = 20
        item_id = f'course_content_{item_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(
            item_id, comments_count_per_page=comments_count_per_page, reversed_ordering=True)
        start = page_number * comments_count_per_page - \
            comments_count_per_page if page_number > 0 else 0
        end = start + comments_count_per_page
        a_page_section_comments = a_page_section_comments[start:end]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(
            item_id)
        pages_count = (comments_count[0] // comments_count_per_page) + 1
        for comment in a_page_section_comments:
            comment['jalali_datetime'], time = date_converter.Date_converter.unix_timestamp_to_jalali(comment['unix_datetime']).split(' ')
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': item_id}

    # comments page
    @fullstack_blueprint.route('/comments/course_info_<course_id>')
    def comments_course_info(course_id):
        user = common.get_user_from_token()
        course_id = f'course_info_{course_id}'
        # replies will have proper depth after get_comments_by_section_id function
        all_comments = comments_orm.Comments.get_comments_by_section_id(course_id)
        return render_template('comments.html', user=user, section_id=course_id)

    @fullstack_blueprint.route('/comments/course_overview_<course_id>', methods=['GET', 'POST'])
    def comments_course_overview(course_id):
        user = common.get_user_from_token()
        course_id = f'course_overview_{course_id}'
        # replies will have proper depth after get_comments_by_section_id function
        all_comments = comments_orm.Comments.get_comments_by_section_id(course_id) 
        return render_template('comments.html', user=user, section_id=course_id)

    @fullstack_blueprint.route('/comments/course_content_<item_id>')
    def comments_course_content(item_id):
        user = common.get_user_from_token()
        item_id = f'course_content_{item_id}'
        # replies will have proper depth after get_comments_by_section_id function
        all_comments = comments_orm.Comments.get_comments_by_section_id(item_id)
        return render_template('comments.html', user=user, section_id=item_id)

    # post comment
    @fullstack_blueprint.route('/post-comment', methods=['POST'])
    def post_comment():
        user = common.get_user_from_token()
        if user == None:
            result = 'not_logged_in'
        # elif user['user_type'] != -2:
        #     result = 'only_admins_are_allowed'
        else:
            comment_text = request.form.get('comment_text', None)
            section_id = request.form.get('section_id', None)
            reply_to = request.form.get('reply_to', None)
            reply_to = int(reply_to)
            comment_replied = comments_orm.Comments.get_comment_by_id(reply_to)
            if comment_replied:
                if comment_replied['reply_to_comment_id'] == -1:
                    new_comment = comments_orm.Comments.insert_new_comment(
                        comment_text=comment_text, sender_name=user['full_name'], sender_id=user['id'], section_id=section_id, reply_to_comment_id=reply_to if reply_to != -1 else -1, unix_datetime=time.time())
                    result = 'succeed'
                else:
                    result = 'you_cant_answer_to_this_comment'
            else:
                new_comment = comments_orm.Comments.insert_new_comment(
                    comment_text=comment_text, sender_name=user['full_name'], sender_id=user['id'], section_id=section_id, reply_to_comment_id=reply_to if reply_to != -1 else -1, unix_datetime=time.time())
                result = 'succeed'

        return {'result': result}

    @fullstack_blueprint.route('/get-admin')
    def get_admin():
        user = common.get_user_from_token()
        if user and (user['user_type'] == -2 or user['user_type'] == -1):
            result = 'admin'
        else:
            result = 'not_admin'
        return {'result': result}

    @fullstack_blueprint.route('/delete-comment', methods=['POST'])
    def delete_comment_post():
        user = common.get_user_from_token()
        comment_id = request.args.get('comment_id')
        comment = comments_orm.Comments.get_comment_by_id(comment_id)
        course_id = comment['section_id'].split('_')[2]
        reply_comments_ids = comments_orm.Comments.get_comments_id_by_reply_to_comment_id(comment_id)
        if reply_comments_ids : # delete the comment with its replies
            comments_orm.Comments.delete_a_comment_by_id(comment_id)
            for element in reply_comments_ids:
                comments_orm.Comments.delete_a_comment_by_id(element['id'])
        else:
            comments_orm.Comments.delete_a_comment_by_id(comment_id)
        if comment['section_id'] == f'course_info_{course_id}' :
            return redirect(url_for('fullstack_blueprint.comments_course_info', course_id=course_id))
        elif comment['section_id'] == f'course_overview_{course_id}' :
            return redirect(url_for('fullstack_blueprint.comments_course_overview', course_id=course_id))
        else :
            item_id = comment['section_id'].split('_')[2]
            return redirect(url_for('fullstack_blueprint.comments_course_content', item_id=item_id))