import time
from flask import redirect, render_template
from routes import common
from models_mysql import courses_orm, items_orm, quizzes_orm, questions_orm, comments_orm, notifications_orm

flash_messages = []

def make_routes(goldis_blueprint):
    @goldis_blueprint.route("/course-info/<course_id>")
    def course_info(course_id):
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        course = None
        section_id = course_id
        for crs in all_courses:
            if str(crs['id']) == str(course_id):
                course = crs
                break
        # comments_orm.Comments.insert_new_comment('سلام چطوری  مطوری پطوری', user_name , user_id , f'course_content_{item_id}', None)
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_content_{course_id}')
        all_notifications = notifications_orm.Notifications.get_notifications_by_section_id(section_id)
        return render_template("course-info.html", course=course, all_notifications=all_notifications, user=user, all_comments=all_comments, flash_messages=flash_messages)

    @goldis_blueprint.route('/course-overview/<course_id>')
    def course_overview(course_id):
        course_id = int(course_id)
        user = common.get_user_from_token()
        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        all_courses = courses_orm.Courses.get_all_courses()
        course = None

        for crs in all_courses:
            if str(crs['id']) == str(course_id):
                course = crs
                print('ok course:', course_id)
                break
        all_comments = []
        return render_template("course-overview.html", course=course, course_items=course_items,user=user, all_comments=all_comments, flash_messages=flash_messages)

    @goldis_blueprint.route('/course-content/<course_id>/<item_id>')
    def course_content(course_id, item_id):
        course_id = int(course_id)
        item_id = int(item_id)
        user = common.get_user_from_token()
        user_id = int(user['id'])
        user_name = user['full_name']
        user_id = None
        if user != None:
            user_id = user['id']
        all_courses = courses_orm.Courses.get_all_courses()
        course = None
        for crs in all_courses:
            if str(crs['id']) == str(course_id):
                course = crs
                break

        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        course_item = None
        for crs_item in course_items:
            if str(crs_item['id']) == str(item_id):
                course_item = crs_item
                break
        # comments_orm.Comments.insert_new_comment('سلام چطوری  مطوری پطوریs', user_name , user_id , f'course_content_{item_id}', None)
        quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_ids(item_id)
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_content_{item_id}')
        last_comments = all_comments[0:19]
        return render_template("course-content.html", user_id=user_id, course=course, course_item=course_item, user=user, all_comments=last_comments, flash_messages=flash_messages, quizzes=quizzes)

    @goldis_blueprint.route("/quiz/<quiz_id>")
    def quiz_content(quiz_id):
        user = common.get_user_from_token()
        last_user_answers = []
        quizzes = quizzes_orm.Quizzes.get_all_quizzes()
        quiz = None
        for qz in quizzes:
            if str(qz['id']) == str(quiz_id):
                quiz = qz
                break
        questions = questions_orm.Questions.get_all_questions_by_ids(quiz_id)

        return render_template("quiz-content.html", user=user, quiz=quiz, flash_messages=flash_messages, questions=questions, last_user_answers=last_user_answers)
