import jdatetime , json, time, tools
from flask import redirect, render_template, request, session, url_for
from routes import common
from models_mysql import courses_orm, items_orm, quizzes_orm, questions_orm, comments_orm, course_news_orm, user_courses_orm, flash_messages_orm, user_quizzes_orm, user_items_orm

flash_messages = []

def make_routes(goldis_blueprint):
    @goldis_blueprint.route("/course-info/course_<course_id>")
    def course_info(course_id):
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        course = None
        section_id = course_id
        for crs in all_courses:
            if str(crs['id']) == str(course_id):
                course = crs
                course['jalali_start_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
                course['jalali_end_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
                break
        if course == None:
            return redirect('/404-not-found') 
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_content_{course_id}')
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(section_id)
        return render_template("course-info.html", course=course, all_courses_news=all_courses_news, user=user, all_comments=all_comments, flash_messages=flash_messages)

    @goldis_blueprint.route('/course-overview/course_<course_id>')
    def course_overview(course_id):
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        else:
            user_full_name = user['full_name']

        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        items_jalali_datetime = []
        for item in course_items:
            item['jalali_start_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(item['unix_start_datetime'])
            item['jalali_end_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(item['unix_end_datetime'])
            items_jalali_datetime.append(item)
        all_courses = courses_orm.Courses.get_all_courses()
        course = None
        for crs in all_courses:
            if str(crs['id']) == str(course_id):
                course = crs
                course['jalali_start_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
                course['jalali_end_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
                break

        user_course = user_courses_orm.User_courses.get_user_course_by_ids(user_id = user['id'], course_id = course_id)
        if not user_course:
            unix_datetime = time.time()
            new_user_course_id = user_courses_orm.User_courses.insert_new_user_course(user_id = user['id'], course_id=course_id,price=course['price'],unix_datetime=unix_datetime)
            
        if course['unix_start_datetime'] >= time.time():
            flash_messages_orm.Flash_messages.insert_new_flash_message(user['g_token'], f'{user_full_name} گرامی زمان شروع این دوره هنوز نرسیده است.', 'danger') 
            return redirect('/')
        if course['unix_end_datetime'] <= time.time():
            flash_messages_orm.Flash_messages.insert_new_flash_message(user['g_token'], f'{user_full_name} گرامی زمان شرکت در این دوره به پایان رسیده است.', 'danger') 
            return redirect('/')
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_overview_{course_id}')
        return render_template("course-overview.html", course=course, course_items=items_jalali_datetime,user=user, all_comments=all_comments, flash_messages=flash_messages)

    @goldis_blueprint.route('/course-content/course_<course_id>/item_<item_id>')
    def course_content(course_id, item_id):
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        user_item = user_items_orm.User_items.get_user_item_by_ids(user_id=user['id'], item_id=item_id)
        if not user_item :
            unix_datetime = time.time()
            new_user_item_id = user_items_orm.User_items.insert_new_user_item(user_id=user['id'], item_id=item_id, unix_datetime=unix_datetime)
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
        # quizzes = quizzes_orm.Quizzes.get_all_quizzes_with_questions(item_id)
        # if quizzes == []:
        quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(item_id)
        quizzes_jalali_datetime = []
        for quiz in quizzes:
            quiz['jalali_start_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(quiz['unix_start_datetime'])
            quiz['jalali_end_datetime'] = tools.Date_converter.unix_timestamp_to_jalali(quiz['unix_end_datetime'])
            quizzes_jalali_datetime.append(quiz)

        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_content_{item_id}')
        last_comments = all_comments[0:19]
        return render_template("course-content.html", course=course, course_item=course_item, user=user, all_comments=last_comments, flash_messages=flash_messages, quizzes=quizzes_jalali_datetime)

    @goldis_blueprint.route("/quiz/quiz_<quiz_id>")
    def quiz_content(quiz_id):
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        unix_datetime = time.time()
        new_user_quiz_id = user_quizzes_orm.User_quizzes.insert_new_user_quiz(user_id=user['id'], quiz_id=quiz_id, unix_datetime=unix_datetime)
        last_user_answers = []
        quizzes = quizzes_orm.Quizzes.get_all_quizzes()
        questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(quiz_id)
        quiz = quizzes_orm.Quizzes.get_quiz_by_id(quiz_id)
        item_id = quiz['item_id']
        item = items_orm.Items.get_item_by_id(item_id)
        course_id = item['course_id']
        return render_template("quiz-content.html", user=user, quiz=quiz, flash_messages=flash_messages, questions=questions, last_user_answers=last_user_answers, course_id=course_id, item_id=item_id, quiz_id=quiz_id)

    @goldis_blueprint.route('/set-user-answers', methods=['POST'])
    def set_user_answers():
        user = common.get_user_from_token()
        course_id = request.args.get('course_id')
        item_id = request.args.get('item_id')
        quiz_id = request.args.get('quiz_id')
        unix_datetime = time.time()
        all_answers = request.form.get('all_answers')
        json_all_answers = json.loads(all_answers)
        string_all_answers = ','.join([str(elem) for i,elem in enumerate(json_all_answers)])
        if string_all_answers:
            user_answers = quizzes_orm.Quizzes.update_quiz(id=quiz_id, user_answers=string_all_answers)
            new_user_quiz_id = user_quizzes_orm.User_quizzes.insert_new_user_quiz(user_id=user['id'], quiz_id=quiz_id, unix_datetime=unix_datetime, user_answers=user_answers)
        return redirect(url_for('goldis_blueprint.course_content', course_id=course_id, item_id=item_id))

    @goldis_blueprint.route('/my-courses')
    def my_courses():
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(user['g_token'])
        user_courses = user_courses_orm.User_courses.get_user_courses_by_user_id(user['id'])
        user_courses_with_title = []
        course = None
        for crs in user_courses:
            course = courses_orm.Courses.get_course_by_id(crs['course_id'])
            crs['title'] = course['title']
            user_courses_with_title.append(crs)
        return render_template('my-courses.html', user=user, courses = user_courses_with_title, flash_messages = flash_messages)
    
    @goldis_blueprint.route('/my-items')
    def my_items():
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(user['g_token'])
        course_id = request.args.get('course_id')
        user_items = user_items_orm.User_items.get_all_user_items_by_ids(user['id'], course_id)
        user_items_with_title = []
        for it in user_items:
            item = items_orm.Items.get_item_by_id(it['item_id'])
            it['title'] = item['title']
            user_items_with_title.append(it)
        return render_template('my-items.html', user=user, items = user_items_with_title, flash_messages = flash_messages, course_id=course_id)

    @goldis_blueprint.route("/quiz-results/item_<item_id>")
    def user_quizzes(item_id):
        user = common.get_user_from_token()
        if user == None:
            flash_messages_orm.Flash_messages.insert_new_flash_message(message='کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', message_type='danger') 
            return redirect('/')
        user_quizzes = user_quizzes_orm.User_quizzes.get_all_user_quizzes_by_ids(user['id'], item_id)
        user_quizzes_jalali_datetime = []
        for quiz in user_quizzes:
            quiz['date'] = tools.Date_converter.unix_timestamp_to_jalali(quiz['unix_datetime'])
            user_quizzes_jalali_datetime.append(quiz)
        return render_template('quiz_results.html', user=user, attender=user, user_quizzes=user_quizzes_jalali_datetime)

    