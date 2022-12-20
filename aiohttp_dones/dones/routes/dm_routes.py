from flask import redirect, render_template, request, url_for, session
from routes import common
import time, secrets
import jdatetime
from models_mysql import users_orm, courses_orm, items_orm, quizzes_orm, questions_orm, comments_orm, notifications_orm

def make_routes(goldis_blueprint):
    def is_admin_user(user):
      is_admin = False
      if user and 'user_type' in user and user['user_type'] == -2:
          is_admin = True
      return is_admin

    @goldis_blueprint.route("/dm-home")
    def dm_home():
        user = common.get_user_from_token()
        return render_template("data_management/dm_home.html", user=user)

    # dm users
    @goldis_blueprint.route("/dm-users")
    def dm_users():
        users = users_orm.Users.get_all_users()
        user = common.get_user_from_token()
        start_index = 2
        page_number = 0
        page_count = 0
        user_id = None
        update_user = None
        return render_template("data_management/dm_users.html", user=user, users=users, update_user= update_user, page_number=page_number, page_count=page_count, start_index=start_index, user_id=user_id) 
    
    @goldis_blueprint.route("/dm-users", methods=['POST'])
    def dm_users_post():
        # (full_name, mobile, g_token, password, sheba_number, credit_score, user_type, invited_friend_mobile, register_datetime):
        user = common.get_user_from_token()
        start_index = 2
        page_number = 0
        page_count = 0
        user_id = None
        update_user = None
        sheba_number = ''
        credit_score = 0
        invited_friend_mobile = ''
        g_token = secrets.token_hex()
        session['g_token'] = g_token
        register_datetime = time.time()
        full_name = request.form.get('full_name', None)
        mobile = request.form.get('mobile', None)
        national_id = request.form.get('national_id', None)
        password = request.form.get('password', None)
        user_type_string = request.form.get('user_type', None)

        if user_type_string == 'ادمین':
            user_type = -2
        elif user_type_string == 'سازمان/گروه':
            user_type = -1
        else:
            user_type = 0

        new_user = users_orm.Users.insert_new_user(full_name=full_name, mobile=mobile, national_id=national_id,password=password,user_type=user_type, g_token=g_token, sheba_number=sheba_number, credit_score=credit_score, invited_friend_mobile=invited_friend_mobile, register_datetime=register_datetime)
        users = users_orm.Users.get_all_users()

        return render_template("data_management/dm_users.html", user=user, users=users, update_user= update_user, page_number=page_number, page_count=page_count, start_index=start_index, user_id=user_id)  

    @goldis_blueprint.route("/dm-users/<user_id>", methods=['GET','POST'])
    def dm_users_edit(user_id):
        user = common.get_user_from_token()
        user_id = int(user_id)
        start_index = 2
        page_number = 0
        page_count = 0
        sheba_number = ''
        credit_score = 0
        invited_friend_mobile = ''
        last_login_datetime = 0
        update_user = users_orm.Users.get_user_by_id(user_id)
        if request.method == 'POST':
            full_name = request.form.get('full_name', None)
            mobile = request.form.get('mobile', None)
            national_id = request.form.get('national_id', None)
            user_type_string = request.form.get('user_type', None)

            if user_type_string == 'ادمین':
                user_type = -2
            elif user_type_string == 'سازمان/گروه':
                user_type = -1
            else:
                user_type = 0
        
            edit_user = users_orm.Users.update_user(id=user_id, full_name=full_name, mobile=mobile, national_id=national_id,user_type=user_type, sheba_number=sheba_number, credit_score=credit_score, invited_friend_mobile=invited_friend_mobile, last_login_datetime=last_login_datetime)
            users = users_orm.Users.get_all_users()
            return redirect('/dm-users')
        else:
            users = users_orm.Users.get_all_users()
            return render_template("data_management/dm_users.html", user=user, users=users, update_user= update_user, page_number=page_number, page_count=page_count, start_index=start_index, user_id=user_id)  

    # dm courses
    @goldis_blueprint.route("/dm-courses")
    def dm_courses():
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        course_id = None
        update_course = None
        return render_template("data_management/dm_courses.html", user=user, all_courses=all_courses, update_course= update_course, course_id=course_id)   

    @goldis_blueprint.route("/dm-courses", methods=['POST'])
    def dm_courses_post():
        user = common.get_user_from_token()
        course_result = None
        course_id = None
        update_course = None

        title = request.form.get('title', None)
        jalali_start_datetime = request.form.get('unix_start_datetime', None)
        jalali_end_datetime = request.form.get('unix_end_datetime', None)
        description = request.form.get('description', None)
        price = request.form.get('price', None)
        image_path = request.form.get('image_path', None)
        logo_path = request.form.get('logo_path', None)
        video_path = request.form.get('video_path', None)
        welcome_text = request.form.get('welcome_text', None)
        body_html = request.form.get('body_html', None)
        institute = request.form.get('institute', None)
        free_items_count = request.form.get('free_items_count', None)

        new_course = courses_orm.Courses.insert_new_course(welcome_text=welcome_text, body_html=body_html, free_items_count=free_items_count,course_result=course_result, title=title, institute=institute, jalali_start_datetime=jalali_start_datetime, jalali_end_datetime=jalali_end_datetime, price=price, logo_path=logo_path, image_path=image_path, description=description, video_path=video_path)
        all_courses = courses_orm.Courses.get_all_courses()
        return render_template("data_management/dm_courses.html", user=user, all_courses=all_courses, update_course= update_course, course_id=course_id)
    # update course
    @goldis_blueprint.route("/dm-courses/<course_id>", methods=['GET','POST'])
    def dm_courses_edit(course_id):
        user = common.get_user_from_token()
        course_id = int(course_id)
        course_result = None
        update_course = courses_orm.Courses.get_course_by_id(course_id)
        
        if request.method == 'POST':
            title = request.form.get('title', None)
            jalali_start_datetime = request.form.get('unix_start_datetime', None)
            jalali_end_datetime = request.form.get('unix_end_datetime', None)
            description = request.form.get('description', None)
            price = request.form.get('price', None)
            image_path = request.form.get('image_path', None)
            logo_path = request.form.get('logo_path', None)
            video_path = request.form.get('video_path', None)
            welcome_text = request.form.get('welcome_text', None)
            body_html = request.form.get('body_html', None)
            institute = request.form.get('institute', None)
            free_items_count = request.form.get('free_items_count', None)

            edit_course = courses_orm.Courses.update_course(id=course_id, welcome_text=welcome_text, body_html=body_html, free_items_count=free_items_count,course_result=course_result, title=title, institute=institute, jalali_start_datetime=jalali_start_datetime, jalali_end_datetime=jalali_end_datetime, price=price, logo_path=logo_path, image_path=image_path, description=description, video_path=video_path)
            all_courses = courses_orm.Courses.get_all_courses()
            return redirect('/dm-courses')
        else:
            all_courses = courses_orm.Courses.get_all_courses()
            return render_template("data_management/dm_courses.html", user=user, all_courses=all_courses, update_course= update_course, course_id=course_id)

    # delete course
    @goldis_blueprint.route("/dm-delete-course/<course_id>")
    def dm_delete_course(course_id):
      course_id = int(course_id)
      courses_orm.Courses.delete_course_by_id(course_id)
      return redirect('/dm-courses')

    # dm items
    @goldis_blueprint.route("/dm-course-items/<course_id>")
    def dm_course_items(course_id):
        course_id = int(course_id)
        user = common.get_user_from_token()
        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        len_course_items = len(course_items) if course_items else None
        course_item_id_edit = None 
        update_course_item = None
        all_course_item_id_link = []
        if course_items:
            for course_item in course_items:
                course_item_id = course_item['id']
                course_item_id_link = f'/dm-delete-course-item/{course_id}/{course_item_id}'
                all_course_item_id_link.append(course_item_id_link)
        return render_template("data_management/dm_course_items.html", user=user, course_items=course_items, update_course_item= update_course_item, course_id=course_id, len=len_course_items, course_item_id=course_item_id_edit, all_course_item_id_link=all_course_item_id_link)   

    @goldis_blueprint.route("/dm-course-items/<course_id>", methods=['POST'])
    def dm_course_items_post(course_id):
        user = common.get_user_from_token()
        course_id = int(course_id)
        course_item_id_edit = None 
        update_course_item = None

        title = request.form.get('title', None)
        jalali_start_datetime = request.form.get('unix_start_datetime', None)
        jalali_end_datetime = request.form.get('unix_end_datetime', None)
        description = request.form.get('description', None)

        new_course_item = items_orm.Items.insert_new_item(course_id=course_id, title=title, jalali_start_datetime=jalali_start_datetime, jalali_end_datetime=jalali_end_datetime, description=description)

        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        len_course_items = len(course_items) if course_items else None
        all_course_item_id_link = []
        if course_items:
            for course_item in course_items:
                course_item_id = course_item['id']
                course_item_id_link = f'/dm-delete-course-item/{course_id}/{course_item_id}'
                all_course_item_id_link.append(course_item_id_link)

        return render_template("data_management/dm_course_items.html", user=user, course_items=course_items, update_course_item= update_course_item, course_id=course_id, len=len_course_items, course_item_id=course_item_id_edit, all_course_item_id_link=all_course_item_id_link)
  
    # update item
    @goldis_blueprint.route("/dm-course-items/<course_id>/<course_item_id>", methods=['GET','POST'])
    def dm_course_items_edit(course_id, course_item_id):
        user = common.get_user_from_token()
        course_id = int(course_id)
        course_item_id = int(course_item_id)
        update_course_item = items_orm.Items.get_item_by_id(course_item_id)

        if request.method == 'POST':
            title = request.form.get('title', None)
            jalali_start_datetime = request.form.get('unix_start_datetime', None)
            jalali_end_datetime = request.form.get('unix_end_datetime', None)
            description = request.form.get('description', None)

            edit_course_item = items_orm.Items.update_item(id=course_item_id, title=title, jalali_start_datetime=jalali_start_datetime, jalali_end_datetime=jalali_end_datetime, description=description)

            course_items = items_orm.Items.get_all_items_by_course_id(course_id)
            return redirect(url_for('goldis_blueprint.dm_course_items', course_id=course_id ))
        else:
            course_items = items_orm.Items.get_all_items_by_course_id(course_id)
            len_course_items = len(course_items) if course_items else None
            all_course_item_id_link = []
            if course_items:
                for course_item in course_items:
                    course_item_id = course_item['id']
                    course_item_id_link = f'/dm-delete-course-item/{course_id}/{course_item_id}'
                    all_course_item_id_link.append(course_item_id_link)
            return render_template("data_management/dm_course_items.html", user=user, course_items=course_items, update_course_item= update_course_item, course_id=course_id, len=len_course_items, course_item_id=course_item_id, all_course_item_id_link=all_course_item_id_link)
 
    # delete item
    @goldis_blueprint.route("/dm-delete-course-item/<course_id>/<course_item_id>")
    def dm_delete_item(course_id, course_item_id):
      course_item_id = int(course_item_id)
      items_orm.Items.delete_item_by_id(course_item_id)
      return redirect(url_for('goldis_blueprint.dm_course_items', course_id=course_id))

    # dm quizzes
    @goldis_blueprint.route("/dm-quiz/<course_item_id>")
    def dm_quiz(course_item_id):
        course_item_id = int(course_item_id)
        user = common.get_user_from_token()
        quizs = quizzes_orm.Quizzes.get_all_quizzes_by_ids(course_item_id)
        quiz_id = None
        update_quiz = None
        return render_template("data_management/dm_quiz.html", user=user, quizs=quizs, course_item_id= course_item_id, update_quiz=update_quiz , quiz_id=quiz_id )   

    @goldis_blueprint.route("/dm-quiz/<course_item_id>", methods=['POST'])
    def dm_quiz_post(course_item_id):
        user = common.get_user_from_token()
        course_item_id = int(course_item_id)
        quiz_id = None
        update_quiz = None

        title = request.form.get('title', None)
        jalali_start_datetime = request.form.get('unix_start_datetime', None)
        jalali_end_datetime = request.form.get('unix_end_datetime', None)
        description = request.form.get('description', None)
        duration = request.form.get('duration', None)
        attendance_max = request.form.get('attendance_max', None)
        quiz_type = request.form.get('quiz_type', None)
        question_count = request.form.get('question_count', None)

        new_quiz = quizzes_orm.Quizzes.insert_new_quiz(item_id=course_item_id, title=title, jalali_start_datetime=jalali_start_datetime, jalali_end_datetime=jalali_end_datetime, description=description, duration=duration, attendance_max=attendance_max, quiz_type=quiz_type, question_count=question_count)
        quizs = quizzes_orm.Quizzes.get_all_quizzes_by_ids(course_item_id)

        return render_template("data_management/dm_quiz.html", user=user, quizs=quizs, course_item_id= course_item_id, update_quiz=update_quiz , quiz_id=quiz_id )

    @goldis_blueprint.route("/dm-delete-quiz/<quiz_id>")
    def dm_delete_quiz(quiz_id):
      quiz_id = int(quiz_id)
      quizzes_orm.Quizzes.delete_quiz_by_id(quiz_id)
      return redirect(url_for('goldis_blueprint.dm_quiz', quiz_id=quiz_id))    
    
    # dm questions
    @goldis_blueprint.route("/dm-question/<quiz_id>")
    def dm_question(quiz_id):
        quiz_id = int(quiz_id)
        user = common.get_user_from_token()
        questions = questions_orm.Questions.get_all_questions_by_ids(quiz_id)
        question_id = None
        question_update = None
        return render_template("data_management/dm_question_pack.html", user=user, question_pack=questions, question_id=question_id, question_update= question_update, quiz_id=quiz_id )   

    @goldis_blueprint.route("/dm-question/<quiz_id>", methods=['POST'])
    def dm_question_post(quiz_id):
        user = common.get_user_from_token()
        quiz_id = int(quiz_id)
        question_id = None
        question_update = None

        question_text = request.form.get('question_text', None)
        answer_number = request.form.get('answer_number', None)
        answer_description = request.form.get('answer_description', None)
        options = request.form.get('options', None)

        new_question = questions_orm.Questions.insert_new_question(quiz_id=quiz_id, question_text=question_text, answer_number=answer_number, answer_description=answer_description, options=options)
        questions = questions_orm.Questions.get_all_questions_by_ids(quiz_id)

        return render_template("data_management/dm_question_pack.html", user=user, question_pack=questions, question_id=question_id, question_update= question_update, quiz_id=quiz_id)

    @goldis_blueprint.route("/dm-delete-question/<quiz_id>/<question_id>")
    def dm_delete_question(quiz_id, question_id):
      question_id = int(question_id)
      quiz_id = int(quiz_id)
      questions_orm.Questions.delete_question_by_id(question_id)
      return redirect(url_for('goldis_blueprint.dm_question', quiz_id=quiz_id))

    
    # dm notifications
    @goldis_blueprint.route("/dm-notifications")
    def dm_notifications():
        user = common.get_user_from_token()
        
        all_notifications = notifications_orm.Notifications.get_all_notifications()
        return render_template("data_management/dm_notification.html", user=user, notifications=all_notifications)   

    @goldis_blueprint.route("/dm-notifications", methods=['POST'])
    def dm_notifications_post():
        user = common.get_user_from_token()
        
        section_id
        jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
        notification_type = request.form.get('notification_type', None)
        notification_text = request.form.get('notification_text', None)

        new_notification = notifications_orm.Notifications.insert_new_notification(section_id=section_id, jalali_date=jalali_date, notification_type=notification_type, notification_text=notification_text)
        all_notifications = notifications_orm.Notifications.get_all_notifications()
        return render_template("data_management/dm_notification.html", user=user, notifications=all_notifications)