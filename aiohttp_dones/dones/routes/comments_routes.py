from models_mysql import  comments_orm
from flask import redirect, render_template
from models_mysql import courses_orm, items_orm, quizzes_orm, questions_orm, comments_orm
from routes import common 

all_notifications = []
flash_messages = []
def make_routes(goldis_blueprint):

    @goldis_blueprint.route('/json-get-comments-and-notifications-by-section-id/course_info_<course_id>')
    def json_get_comments_and_notifications_by_section_id(course_id):
        # section_id = request.match_info.get('section_id', None)
        # page_number = request.query.get('page_number', '1')
        # all_notifications = await model_aioredis.Notifications.get_all_notifications_by_section_id(self._app, section_id)
        # page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        page_number = None
        comments_count_per_page = 20
        course_id = f'course_info_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(course_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(course_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id, 'all_notifications':all_notifications}


    @goldis_blueprint.route('/json-get-comments-and-notifications-by-section-id/course_overview_<course_id>')
    def json_get_comments_and_notifications_by_section_id2(course_id):
        page_number = None
        comments_count_per_page = 20
        course_id = f'course_overview_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(course_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(course_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': course_id, 'all_notifications':all_notifications}

    @goldis_blueprint.route('/json-get-comments-and-notifications-by-section-id/course_content_<item_id>')
    def json_get_comments_and_notifications_by_section_id3(item_id):
        page_number = None
        comments_count_per_page = 20
        item_id = f'course_content_{item_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(item_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(item_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        return {'all_comments': a_page_section_comments, 'pages_count': pages_count, 'current_page': page_number, 'section_id': item_id, 'all_notifications':all_notifications}

    # comments page
    @goldis_blueprint.route('/comments/course_info_<course_id>')
    def comments_course_info(course_id):
        user = common.get_user_from_token()
        page_number = None
        comments_count_per_page = 20
        course_id = f'course_info_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(course_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(course_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        all_comments = comments_orm.Comments.get_comments_by_section_id(course_id) 
        return render_template('comments.html', user=user, all_comments=all_comments, pages_count=pages_count, current_page=page_number, flash_messages=flash_messages, section_id=course_id)

    @goldis_blueprint.route('/comments/course_overview_<course_id>')
    def comments_course_overview(course_id):
        user = common.get_user_from_token()
        page_number = None
        comments_count_per_page = 20
        course_id = f'course_overview_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(course_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(course_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        all_comments = comments_orm.Comments.get_comments_by_section_id(course_id) 
        return render_template('comments.html', user=user, all_comments=all_comments, pages_count=pages_count, current_page=page_number, flash_messages=flash_messages, section_id=course_id)

    @goldis_blueprint.route('/comments/course_content_<course_id>')
    def comments_course_content(course_id):
        user = common.get_user_from_token()
        page_number = None
        comments_count_per_page = 20
        course_id = f'course_content_{course_id}'
        a_page_section_comments = comments_orm.Comments.get_comments_by_section_id(course_id, page_number= None, comments_count_per_page= comments_count_per_page, reversed_ordering= True)
        if page_number == None:
            a_page_section_comments = a_page_section_comments[0:19]
        comments_count = comments_orm.Comments.get_comments_count_by_section_id(course_id)
        pages_count = (comments_count[0] // comments_count_per_page)
        all_comments = comments_orm.Comments.get_comments_by_section_id(course_id) 
        return render_template('comments.html', user=user, all_comments=all_comments, pages_count=pages_count, current_page=page_number, flash_messages=flash_messages, section_id=course_id)