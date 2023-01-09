from flask import redirect, render_template, request, url_for, session
from routes import common
import tools.date_converter as date_converter
import time, secrets, json
from models_mysql import users_orm, courses_orm, items_orm, quizzes_orm, questions_orm, user_courses_orm, course_news_orm, user_quizzes_orm, transactions_orm

def make_routes(fullstack_blueprint):
    def is_admin_user(user):
        is_admin = False
        if user and 'user_type' in user and (user['user_type'] == -2 or user['user_type'] == -1):
            is_admin = True
        return is_admin

    @fullstack_blueprint.route("/dm-home")
    def dm_home():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        return render_template("data_management/dm_home.html", user=user)

    # dm users
    @fullstack_blueprint.route("/dm-users")
    def dm_users():
        users = users_orm.Users.get_all_users_reverse()
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        return render_template("data_management/dm_users.html", user=user, users=users)
    
    @fullstack_blueprint.route("/json-get-dm-users")
    def json_get_dm_users():
        page_number = request.args.get('page_number', '1')
        page_number = int(page_number) if str.isdigit(str(page_number)) else 1
        number_users_per_page = 1
        users_count = users_orm.Users.get_users_count()[0]
        page_count = (users_count // number_users_per_page) + 1
        if page_number != None:
            # start = page_number * users_count - \
            #         users_count if page_number > 0 else 0
            # end = start + number_users_per_page 
            # all_users = users_orm.Users.get_all_users_reverse()
            # a_page_users = a_page_users[start:end]
            all_users = users_orm.Users.get_all_users_reverse()
        return {'page_number':page_number, 'current_page':page_count, 'all_users':all_users, 'number_users_per_page': number_users_per_page}

    @fullstack_blueprint.route("/dm-users", methods=['POST'])
    def dm_users_post():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        g_token = secrets.token_hex()
        register_datetime = time.time()
        full_name = request.form.get('full_name', None)
        mobile = request.form.get('mobile', None)
        password = request.form.get('password', None)
        user_type = request.form.get('user_type', None)
        user = users_orm.Users.get_user_by_mobile(mobile) 
        users = users_orm.Users.get_all_users_reverse()
        if user:
            status = 'mobile_already_exists'
            return render_template("data_management/dm_users.html", user=user, users=users, status=status)
        new_user = users_orm.Users.insert_new_user(full_name=full_name, mobile=mobile, password=password, user_type=user_type, g_token=g_token, register_datetime=register_datetime)
        return redirect('/dm-users')

    @fullstack_blueprint.route("/dm-users/<user_id>", methods=['GET', 'POST'])
    def dm_users_edit(user_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        users_count = users_orm.Users.get_users_count()
        update_user = users_orm.Users.get_user_by_id(user_id)
        if request.method == 'POST':
            full_name = request.form.get('full_name', None)
            mobile = request.form.get('mobile', None)
            user_type = request.form.get('user_type', None)
            edit_user = users_orm.Users.update_user(id=user_id, full_name=full_name, mobile=mobile, user_type=user_type)
            users = users_orm.Users.get_all_users_reverse()
            return redirect('/dm-users')
        else:
            users = users_orm.Users.get_all_users_reverse()
            return render_template("data_management/dm_users.html", user=user, users=users, update_user=update_user, user_id=user_id)

    # dm courses
    @fullstack_blueprint.route("/dm-courses")
    def dm_courses():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        all_courses = courses_orm.Courses.get_all_courses()
        for course in all_courses:
            course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
            course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
        return render_template("data_management/dm_courses.html", user=user, all_courses=all_courses)

    @fullstack_blueprint.route("/dm-courses", methods=['POST'])
    def dm_courses_post():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        course_result = None
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
        def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
        unix_start_datetime = jalali_to_unix(jalali_start_datetime)
        unix_end_datetime = jalali_to_unix(jalali_end_datetime)
        new_course = courses_orm.Courses.insert_new_course(welcome_text=welcome_text, body_html=body_html, title=title, institute=institute,
                                                           unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, price=price, logo_path=logo_path, image_path=image_path, description=description, video_path=video_path)
        return redirect('/dm-courses')

    # update course
    @fullstack_blueprint.route("/dm-courses/<course_id>", methods=['GET', 'POST'])
    def dm_courses_edit(course_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        if request.method == 'POST':
            title = request.form.get('title', None)
            jalali_start_datetime = request.form.get(
                'unix_start_datetime', None)
            jalali_end_datetime = request.form.get('unix_end_datetime', None)
            description = request.form.get('description', None)
            price = request.form.get('price', None)
            image_path = request.form.get('image_path', None)
            logo_path = request.form.get('logo_path', None)
            video_path = request.form.get('video_path', None)
            welcome_text = request.form.get('welcome_text', None)
            body_html = request.form.get('body_html', None)
            institute = request.form.get('institute', None)
            def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
            unix_start_datetime = jalali_to_unix(jalali_start_datetime)
            unix_end_datetime = jalali_to_unix(jalali_end_datetime)
            edit_course = courses_orm.Courses.update_course(id=course_id, welcome_text=welcome_text, body_html=body_html, title=title, institute=institute,
                                                            unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, price=price, logo_path=logo_path, image_path=image_path, description=description, video_path=video_path)
            return redirect('/dm-courses')
        else: 
            update_course = courses_orm.Courses.get_course_by_id(course_id)
            update_course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_course['unix_start_datetime'])
            update_course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_course['unix_end_datetime'])
            all_courses = courses_orm.Courses.get_all_courses()
            for course in all_courses:
                course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
                course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
            return render_template("data_management/dm_courses.html", user=user, all_courses=all_courses, update_course=update_course, course_id=course_id)

    # delete course
    @fullstack_blueprint.route("/dm-delete-course/<course_id>")
    def dm_delete_course(course_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        course_id = int(course_id)
        courses_orm.Courses.delete_course_by_id(course_id)
        return redirect('/dm-courses')

    # dm items
    @fullstack_blueprint.route("/dm-course-items/<course_id>")
    def dm_course_items(course_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        len_course_items = len(course_items) if course_items else None
        for item in course_items:
            item['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_start_datetime'])
            item['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_end_datetime'])
        return render_template("data_management/dm_course_items.html", user=user, course_items=course_items, course_id=course_id, len=len_course_items)

    @fullstack_blueprint.route("/dm-course-items/<course_id>", methods=['POST'])
    def dm_course_items_post(course_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        title = request.form.get('title', None)
        jalali_start_datetime = request.form.get('unix_start_datetime', None)
        jalali_end_datetime = request.form.get('unix_end_datetime', None)
        description = request.form.get('description', None)
        def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
        unix_start_datetime = jalali_to_unix(jalali_start_datetime)
        unix_end_datetime = jalali_to_unix(jalali_end_datetime)
        new_course_item = items_orm.Items.insert_new_item(
            course_id=course_id, title=title, unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, description=description)
        return redirect(url_for('fullstack_blueprint.dm_course_items', course_id=course_id))

    # update item
    @fullstack_blueprint.route("/dm-course-items/<course_id>/<course_item_id>", methods=['GET', 'POST'])
    def dm_course_items_edit(course_id, course_item_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        if request.method == 'POST':
            title = request.form.get('title', None)
            jalali_start_datetime = request.form.get(
                'unix_start_datetime', None)
            jalali_end_datetime = request.form.get('unix_end_datetime', None)
            description = request.form.get('description', None)
            def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
            unix_start_datetime = jalali_to_unix(jalali_start_datetime)
            unix_end_datetime = jalali_to_unix(jalali_end_datetime)
            edit_course_item = items_orm.Items.update_item(
                id=course_item_id, title=title, unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, description=description)
            course_items = items_orm.Items.get_all_items_by_course_id(
                course_id)
            return redirect(url_for('fullstack_blueprint.dm_course_items', course_id=course_id))
        else:
            course_items = items_orm.Items.get_all_items_by_course_id(
                course_id)
            update_course_item = items_orm.Items.get_item_by_id(course_item_id)
            update_course_item['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_course_item['unix_start_datetime'])
            update_course_item['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_course_item['unix_end_datetime'])
            len_course_items = len(course_items) if course_items else None
            for item in course_items:
                item['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_start_datetime'])
                item['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_end_datetime'])
            return render_template("data_management/dm_course_items.html", user=user, course_items=course_items, update_course_item=update_course_item, course_id=course_id, len=len_course_items, course_item_id=course_item_id)

    # delete item
    @fullstack_blueprint.route("/dm-delete-course-item/<course_id>/<course_item_id>")
    def dm_delete_item(course_id, course_item_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        course_item_id = int(course_item_id)
        items_orm.Items.delete_item_by_id(course_item_id)
        return redirect(url_for('fullstack_blueprint.dm_course_items', course_id=course_id))

    # dm quizzes
    @fullstack_blueprint.route("/dm-quiz/<course_item_id>")
    def dm_quiz(course_item_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False: return redirect('/404-not-found')
        quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(course_item_id)
        for quiz in quizzes:
            quiz['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_start_datetime'])
            quiz['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_end_datetime'])
        return render_template("data_management/dm_quiz.html", user=user, quizs=quizzes, course_item_id= course_item_id)   

    @fullstack_blueprint.route("/dm-quiz/<course_item_id>", methods=['POST'])
    def dm_quiz_post(course_item_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        title = request.form.get('title', None)
        jalali_start_datetime = request.form.get('unix_start_datetime', None)
        jalali_end_datetime = request.form.get('unix_end_datetime', None)
        description = request.form.get('description', None)
        duration = request.form.get('duration', None)
        attendance_max = request.form.get('attendance_max', None)
        quiz_type = request.form.get('quiz_type', None)
        question_count = request.form.get('question_count', None)
        def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
        unix_start_datetime = jalali_to_unix(jalali_start_datetime)
        unix_end_datetime = jalali_to_unix(jalali_end_datetime)
        new_quiz = quizzes_orm.Quizzes.insert_new_quiz(item_id=course_item_id, title=title, unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, description=description, duration=duration, attendance_max=attendance_max, quiz_type=quiz_type, question_count=question_count)
        return redirect(url_for('fullstack_blueprint.dm_quiz', course_item_id=course_item_id))

    @fullstack_blueprint.route("/dm-quiz/<course_item_id>/<quiz_id>", methods=['GET', 'POST'])
    def edit_quiz(course_item_id, quiz_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        if request.method == 'POST':
            title = request.form.get('title', None)
            jalali_start_datetime = request.form.get(
                'unix_start_datetime', None)
            jalali_end_datetime = request.form.get('unix_end_datetime', None)
            description = request.form.get('description', None)
            duration = request.form.get('duration', None)
            attendance_max = request.form.get('attendance_max', None)
            quiz_type = request.form.get('quiz_type', None)
            question_count = request.form.get('question_count', None)
            def jalali_to_unix(data_time):
                datetime = data_time.split('/')
                gregorian_datetime = date_converter.Date_converter.jalali_to_gregorian(int(datetime[0]), int(datetime[1]), int(datetime[2]))
                unix_datetime = date_converter.Date_converter.gregorian_to_unix_timestamp(int(gregorian_datetime[0]), int(gregorian_datetime[1]), int(gregorian_datetime[2]))
                return unix_datetime
            unix_start_datetime = jalali_to_unix(jalali_start_datetime)
            unix_end_datetime = jalali_to_unix(jalali_end_datetime)
            edit_quiz = quizzes_orm.Quizzes.update_quiz(id=quiz_id, title=title, unix_start_datetime=unix_start_datetime, unix_end_datetime=unix_end_datetime, description=description, duration=duration, attendance_max=attendance_max, quiz_type=quiz_type, question_count=question_count)
            
            quizs = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(course_item_id)
            return redirect(url_for('fullstack_blueprint.dm_quiz', course_item_id=course_item_id))
        else:
            update_quiz = quizzes_orm.Quizzes.get_quiz_by_id(quiz_id)
            update_quiz['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_quiz['unix_start_datetime'])
            update_quiz['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(update_quiz['unix_end_datetime'])
            quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(course_item_id)
            for quiz in quizzes:
                quiz['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_start_datetime'])
                quiz['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_end_datetime'])
            return render_template("data_management/dm_quiz.html", user=user, quizs=quizzes, course_item_id= course_item_id, update_quiz=update_quiz , quiz_id=quiz_id)
    
    @fullstack_blueprint.route("/dm-delete-quiz/<course_item_id>/<quiz_id>")
    def dm_delete_quiz(course_item_id, quiz_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        quizzes_orm.Quizzes.delete_quiz_by_id(quiz_id)
        return redirect(url_for('fullstack_blueprint.dm_quiz', course_item_id=course_item_id))

    # dm questions
    @fullstack_blueprint.route("/dm-question/<quiz_id>")
    def dm_question(quiz_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(quiz_id)
        return render_template("data_management/dm_question_pack.html", user=user, question_pack=questions, quiz_id=quiz_id)

    @fullstack_blueprint.route("/dm-question/<quiz_id>", methods=['POST'])
    def dm_question_post(quiz_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        question_text = request.form.get('question_text', None)
        answer_number = request.form.get('answer_number', None)
        answer_description = request.form.get('answer_description', None)
        options = request.form.get('options', None)
        new_question = questions_orm.Questions.insert_new_question(
            quiz_id=quiz_id, question_text=question_text, answer_number=answer_number, answer_description=answer_description, options=options)
        questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(quiz_id)
        return redirect(url_for('fullstack_blueprint.dm_question', quiz_id=quiz_id))

    @fullstack_blueprint.route("/dm-question/<quiz_id>/<question_id>", methods=['GET', 'POST'])
    def edit_question(quiz_id, question_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        if request.method == 'POST':
            question_text = request.form.get('question_text', None)
            answer_number = request.form.get('answer_number', None)
            answer_description = request.form.get('answer_description', None)
            options = request.form.get('options', None)
            edit_question = questions_orm.Questions.update_question(
                id=question_id, question_text=question_text, answer_number=answer_number, answer_description=answer_description, options=options)
            questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(
                quiz_id)
            return redirect(url_for('fullstack_blueprint.dm_question', quiz_id=quiz_id))
        else:
            question_update = questions_orm.Questions.get_question_by_id(
                question_id)
            questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(
                quiz_id)
            return render_template("data_management/dm_question_pack.html", user=user, question_pack=questions, question_id=question_id, question_update=question_update, quiz_id=quiz_id)

    @fullstack_blueprint.route("/dm-delete-question/<quiz_id>/<question_id>")
    def dm_delete_question(quiz_id, question_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        questions_orm.Questions.delete_question_by_id(question_id)
        return redirect(url_for('fullstack_blueprint.dm_question', quiz_id=quiz_id))

    @fullstack_blueprint.route("/dm-courses_news")
    def dm_courses_news():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        all_courses = courses_orm.Courses.get_all_courses()
        all_courses_news = course_news_orm.Courses_news.get_all_courses_news()
        for course_news in all_courses_news:
            course_news['jalali_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course_news['unix_datetime'])
        return render_template("data_management/dm_courses_news.html", user=user, courses_news=all_courses_news, all_courses=all_courses)   

    @fullstack_blueprint.route("/dm-courses_news", methods=['POST'])
    def dm_courses_news_post():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        all_courses = courses_orm.Courses.get_all_courses()
        section_id = request.form.get('section_options', None)
        if section_id != 'home_page':
            for course in all_courses:
                if str(course['id']) == section_id:
                    section_id = f'course_info_{course["id"]}'
        unix_datetime = time.time()
        course_news_text = request.form.get('course_news_text', None)
        new_course_news = course_news_orm.Courses_news.insert_new_course_news(section_id=section_id, unix_datetime=unix_datetime, course_news_text=course_news_text)
        return redirect(url_for("fullstack_blueprint.dm_courses_news"))

    @fullstack_blueprint.route("/dm-courses_news/<section_id>/<notif_id>", methods=['GET','POST'])
    def edit_course_news(section_id, notif_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        if request.method == 'POST':
                section_id = request.form.get('section_options',None)
                all_courses = courses_orm.Courses.get_all_courses()
                if section_id != 'home_page':
                    for course in all_courses:
                        if str(course['id']) == section_id:
                            section_id = f'course_info_{course["id"]}'
                unix_datetime = time.time()
                course_news_text = request.form.get('course_news_text', None)
                new_course_news = course_news_orm.Courses_news.update_course_news(id=notif_id, section_id=section_id, unix_datetime=unix_datetime, course_news_text=course_news_text)
                return redirect(url_for("fullstack_blueprint.dm_courses_news"))
        else:
            course_news =  course_news_orm.Courses_news.get_course_news_by_id(notif_id)
            return render_template("data_management/dm_courses_news.html", user=user, course_news=course_news, section_id=section_id, notif_id=notif_id)

    @fullstack_blueprint.route("/dm-delete-course_news/<section_id>/<course_news_id>")
    def dm_delete_course_news(section_id, course_news_id):
      user = common.get_user_from_token()
      if is_admin_user(user) == False: return redirect('/404-not-found')
      course_news_orm.Courses_news.delete_course_news_by_id(course_news_id)
      return redirect(url_for('fullstack_blueprint.dm_courses_news', section_id=section_id))

    @fullstack_blueprint.route("/dm-courses_news/<section_id>")
    def dm_course_news(section_id):
        user = common.get_user_from_token()
        status = None
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        all_courses = courses_orm.Courses.get_all_courses()
        course_news = course_news_orm.Courses_news.get_courses_news_by_section_id(section_id)
        course_id = section_id.split('_')[2]
        course = courses_orm.Courses.get_course_by_id(course_id)
        return render_template("data_management/dm_courses_news.html", user=user, course_news=course_news, all_courses=all_courses, course=course)
    
    @fullstack_blueprint.route("/dm-quiz-users-answers/<quiz_id>")
    @fullstack_blueprint.route("/quiz-registered-users/<quiz_id>")
    def quiz_results(quiz_id):
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        quiz = user_quizzes_orm.User_quizzes.get_user_quiz_by_quiz_id(user['id'], quiz_id)
        user_quizzes = None
        if quiz:
            item_id = quiz['item_id']
            user_quizzes = user_quizzes_orm.User_quizzes.get_all_user_quizzes_by_ids(user['id'], item_id)
        registered_users = user_quizzes_orm.User_quizzes.get_all_registered_users_by_quiz_id(
            quiz_id)
        for user in registered_users:
                user['jalali_date'] = date_converter.Date_converter.unix_timestamp_to_jalali(user['unix_datetime'])
        all_answers = user_quizzes_orm.User_quizzes.get_all_user_results_by_ids(
            user_id=user['id'], quiz_id=quiz_id)
        all_answers = json.dumps(all_answers)
        questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(quiz_id)
        return render_template('data_management/dm_quiz_registered_users.html', user=user, quiz_id=quiz_id, all_quizzes=user_quizzes, all_answers=all_answers, registered_users=registered_users, questions=questions)

    @fullstack_blueprint.route("/dm-transactions")
    def dm_transactions():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        all_transactions = transactions_orm.Transactions.get_all_transactions_reverse_with_users()
        for transaction in all_transactions:
            course = courses_orm.Courses.get_course_by_id(transaction['course_id'])
            transaction['course_title'] = course['title']
            transaction['jalali_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(transaction['create_datetime'])
        return render_template('data_management/dm_transactions.html', user=user, all_transactions=all_transactions)

    @fullstack_blueprint.route('/dm-notifications')
    def dm_notifications():
        user = common.get_user_from_token()
        if is_admin_user(user) == False:
            return redirect('/404-not-found')
        return render_template('data_management/dm_notifications.html', user=user)

    @fullstack_blueprint.route('/dm-notifications', methods=['POST'])
    def dm_notifications_post():
        
      return redirect(url_for('fullstack_blueprint.dm_notifications'))