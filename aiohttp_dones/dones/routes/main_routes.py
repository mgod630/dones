from flask import redirect, render_template, request, url_for, g, jsonify, Response
from routes import common
from models_mysql import users_orm, accounts_orm, assets_orm, courses_orm, notifications_orm, quizzes_orm, questions_orm, comments_orm


def make_routes(goldis_blueprint):
    @goldis_blueprint.route("/")
    @goldis_blueprint.route("/home")
    def home():
        flash_messages = []
        db_number = 1
        user = common.get_user_from_token()
        # test
        # users_orm.Users.delete_all_users()
        print(users_orm.Users.get_all_users())
        # users_orm.Users.update_user(11, user_type= '-2' )
        # user_update2 = users_orm.Users.get_user_by_id(11)
        # print(user_update2)
        # courses_orm.Courses.insert_new_course('خوش آمدید به درس بلاکچین', 'body html', 'free_items_count', 'course_result','blockchian','goldis','1401/05/03','1401/05/13','0','https://goldis.ir/static/template/goldis-logo-horizontal.png','https://prod-discovery.edx-cdn.org/media/course/image/4321da5b-57d7-49f7-abe1-3ad1c6c3abd9-cb9d6e5bef65.small.png','description')
        # items_orm.Items.insert_new_item(5,'جلسه 8', '1401/03/05', '1401/03/20' , 'آشنایی با مفاهیم 8' )
        # quizzes_orm.Quizzes.insert_new_quiz(1,'آزمون 1', '1401/03/06', '1401/03/25' , 'آزمون بلاکچین 1', '5', '50', '3' )
        # quizzes_orm.Quizzes.update_quiz(3,'آزمون 3', '1401/03/09', '1401/03/28' , 'آزمون بلاکچین 2', '15', '40', '7' )
        # questions_orm.Questions.insert_new_question(1,'سوال 2 :  بلاکچین چیست؟', 'گزینه 1|&|گزینه2|&|گزینه3|&|گزینه 4', None , None)
        # questions_orm.Questions.update_question(8,'سوال 3 :  خانواده چطورن؟' , 'گزینه 1|&|گزینه2|&|گزینه3|&|گزینه 4', None , None)
        # questions_orm.Questions.delete_all_questions()
        # user_account = accounts_orm.Accounts.get_account_by_user_id(user['id'])
        # comments_orm.Comments.delete_all_comments()
        # courses_orm.Courses.delete_course_by_id(5)
        # users_orm.Users.delete_user_by_id(24)

        all_courses = courses_orm.Courses.get_all_courses()
        section_id = '0'
        all_notifications = notifications_orm.Notifications.get_notifications_by_section_id(section_id)
        return render_template("index.html", user=user, user_account=None, all_courses=all_courses, all_notifications=all_notifications, flash_messages=flash_messages, db_number=db_number)

    @goldis_blueprint.route("/landing_page")
    def landing_page():
        user = common.get_user_from_token()
        return render_template('landing_page.html', user=user)
