from models_mysql import comments_orm
from flask import redirect, render_template, request
from models_mysql import courses_orm, items_orm, course_news_orm, questions_orm, comments_orm
from routes import common


def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_info_<course_id>')
    def json_get_comments_and_courses_news_by_section_id(course_id):
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
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id, 'all_courses_news': all_courses_news}

    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_overview_<course_id>')
    def json_get_comments_and_courses_news_by_section_id2(course_id):
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        comments_count_per_page = 20
        section_id = course_id
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
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(
            section_id)
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id, 'all_courses_news': all_courses_news}

    @fullstack_blueprint.route('/json-get-comments-and-courses_news-by-section-id/course_content_<item_id>')
    def json_get_comments_and_courses_news_by_section_id3(item_id):
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        comments_count_per_page = 20
        section_id = item_id
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
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(
            section_id)
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': item_id, 'all_courses_news': all_courses_news}

    # comments page
    @fullstack_blueprint.route('/comments/course_info_<course_id>')
    def comments_course_info(course_id):
        user = common.get_user_from_token()
        course_id = f'course_info_{course_id}'
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            course_id)
        return render_template('comments.html', user=user, all_comments=all_comments, section_id=course_id)

    @fullstack_blueprint.route('/comments/course_overview_<course_id>', methods=['GET', 'POST'])
    def comments_course_overview(course_id):
        user = common.get_user_from_token()
        course_id = f'course_overview_{course_id}'
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            course_id)
        return render_template('comments.html', user=user, all_comments=all_comments, section_id=course_id)

    @fullstack_blueprint.route('/comments/course_content_<course_id>')
    def comments_course_content(course_id):
        user = common.get_user_from_token()
        course_id = f'course_content_{course_id}'
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            course_id)
        return render_template('comments.html', user=user, all_comments=all_comments, section_id=course_id)

    # post comment
    @fullstack_blueprint.route('/post-comment', methods=['POST'])
    def post_comment():
        user = common.get_user_from_token()
        if user == None:
            result = 'not_logged_in'
        elif user['user_type'] != -2:
            result = 'only_admins_are_allowed'
        else:
            comment_text = request.form.get('comment_text', None)
            section_id = request.form.get('section_id', None)
            reply_to = request.form.get('reply_to', None)
            reply_to = int(reply_to)
            comment_replied = comments_orm.Comments.get_comment_by_id(reply_to)
            if comment_replied:
                if comment_replied['reply_to_comment_id'] == -1:
                    new_comment = comments_orm.Comments.insert_new_comment(
                        comment_text=comment_text, sender_name=user['full_name'], sender_id=user['id'], section_id=section_id, reply_to_comment_id=reply_to if reply_to != -1 else -1)
                    result = 'succeed'
                else:
                    result = 'you_cant_answer_to_this_comment'
            else:
                new_comment = comments_orm.Comments.insert_new_comment(
                    comment_text=comment_text, sender_name=user['full_name'], sender_id=user['id'], section_id=section_id, reply_to_comment_id=reply_to if reply_to != -1 else -1)
                result = 'succeed'

        return {'result': result}

    @fullstack_blueprint.route('/delete-comment', methods=['GET', 'POST'])
    def get_admin():
        user = common.get_user_from_token()
        if user['user_type'] == -2:
            result = 'admin'
        else:
            result = 'not admin'
        return {'result': result}
