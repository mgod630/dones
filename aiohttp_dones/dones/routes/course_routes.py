import jdatetime , json, time, tools.date_converter as date_converter
from flask import redirect, render_template, request, session, url_for, flash
from routes import common
from models_mysql import courses_orm, items_orm, quizzes_orm, questions_orm, notifications_orm, course_news_orm, user_courses_orm ,user_quizzes_orm, user_items_orm

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route("/course-info/course_<course_id>")
    def course_info(course_id):
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        course = None
        section_id = f'course_info_{course_id}' 
        course = courses_orm.Courses.get_course_by_id(course_id)
        course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
        course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
        if course == None:
            return redirect('/404-not-found') 
        # unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])[0]
        return render_template("course-info.html", course=course, user=user)

    @fullstack_blueprint.route('/course-overview/course_<course_id>')
    def course_overview(course_id):
        user = common.get_user_from_token()
        course = courses_orm.Courses.get_course_by_id(course_id)
        if user == None and course['price'] != 0:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        
        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        for item in course_items:
            item['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_start_datetime'])
            item['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(item['unix_end_datetime'])
        
        course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_start_datetime'])
        course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(course['unix_end_datetime'])
        if user:
            user_full_name = user['full_name']
            user_course = user_courses_orm.User_courses.get_user_course_by_ids(user_id = user['id'], course_id = course_id)
            if not user_course :
                if course['price'] == 0 :
                    unix_datetime = time.time()
                    new_user_course_id = user_courses_orm.User_courses.insert_new_user_course(user_id = user['id'], course_id=course_id,price=course['price'],unix_datetime=unix_datetime)
                else:
                    flash(f'{user_full_name} گرامی برای دسترسی به این دوره ابتدا باید آن را خریداری کنید.', 'danger')
                    return redirect(url_for('fullstack_blueprint.course_info', course_id=course_id))
            
            if course['unix_start_datetime'] >= time.time():
                flash(f'{user_full_name} گرامی زمان شروع این دوره هنوز نرسیده است.', 'danger')
                return redirect('/')
            if course['unix_end_datetime'] <= time.time():
                flash(f'{user_full_name} گرامی زمان شرکت در این دوره به پایان رسیده است.', 'danger')
                return redirect('/')

        if course['unix_start_datetime'] >= time.time():
                flash('کاربر گرامی زمان شروع این دوره هنوز نرسیده است.', 'danger')
                return redirect('/')
        if course['unix_end_datetime'] <= time.time():
            flash('کاربر گرامی زمان شروع این دوره هنوز نرسیده است.', 'danger')
            return redirect('/')
        
        # unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])[0]
        return render_template("course-overview.html", course=course, course_items=course_items,user=user)

    @fullstack_blueprint.route('/course-content/course_<course_id>/item_<item_id>')
    def course_content(course_id, item_id):
        user = common.get_user_from_token()
        course = courses_orm.Courses.get_course_by_id(course_id)
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        else:
            user_full_name = user['full_name']
            user_course = user_courses_orm.User_courses.get_user_course_by_ids(user_id = user['id'], course_id = course_id)
            user_item = user_items_orm.User_items.get_user_item_by_ids(user_id=user['id'], item_id=item_id)
            if not user_course:
                if course['price'] != 0 :
                    flash(f'{user_full_name} گرامی برای دسترسی به این دوره ابتدا باید آن را خریداری کنید.', 'danger')
                return redirect(url_for('fullstack_blueprint.course_info', course_id=course_id))
            if not user_item :
                unix_datetime = time.time()
                new_user_item_id = user_items_orm.User_items.insert_new_user_item(user_id=user['id'], item_id=item_id, unix_datetime=unix_datetime)
        # unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])[0]
        course_items = items_orm.Items.get_all_items_by_course_id(course_id)
        course_item = None
        for crs_item in course_items:
            if str(crs_item['id']) == str(item_id):
                course_item = crs_item
                break
        quizzes = None
        if course_item:
            quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(item_id)
            for quiz in quizzes:
                quiz['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_start_datetime'])
                quiz['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_end_datetime'])
            return render_template("course-content.html", course=course, course_item=course_item, user=user, quizzes=quizzes)
        else:
            flash('کاربر گرامی برای این دوره تاکنون جلسه ای تعریف نشده است.', 'warning')
            return redirect(url_for('fullstack_blueprint.course_overview', course_id=course_id))

    @fullstack_blueprint.route("/quiz/quiz_<quiz_id>")
    def quiz_content(quiz_id):
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        else:
            user_full_name = user['full_name']
        quiz = quizzes_orm.Quizzes.get_quiz_by_id(quiz_id)
        item_id = quiz['item_id']
        item = items_orm.Items.get_item_by_id(item_id)
        course_id = item['course_id']
        course = courses_orm.Courses.get_course_by_id(course_id)
        user_course = user_courses_orm.User_courses.get_user_course_by_ids(user_id = user['id'], course_id = course_id)
        if not user_course:
            if course['price'] != 0 :
                flash(f'{user_full_name} گرامی برای دسترسی به این دوره ابتدا باید آن را خریداری کنید.', 'danger')
            return redirect(url_for('fullstack_blueprint.course_info', course_id=course_id))
        unix_datetime = time.time()
        new_user_quiz_id = user_quizzes_orm.User_quizzes.insert_new_user_quiz(user_id=user['id'], quiz_id=quiz_id, unix_datetime=unix_datetime)
        last_user_answers = []
        questions = questions_orm.Questions.get_all_questions_by_id_quiz_id(quiz_id)
        return render_template("quiz-content.html", user=user, quiz=quiz, questions=questions, last_user_answers=last_user_answers, course_id=course_id, item_id=item_id, quiz_id=quiz_id)

    @fullstack_blueprint.route('/set-user-answers', methods=['POST'])
    def send_user_answers():
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
            new_user_quiz_id = user_quizzes_orm.User_quizzes.insert_new_user_quiz(user_id=user['id'], quiz_id=quiz_id, unix_datetime=unix_datetime, user_answers=string_all_answers)
        if all_answers:
            flash(f'{user["full_name"]} گرامی پاسخ های شما با موفقیت ثبت گردید.', 'success')
        else:
            flash(f'{user["full_name"]} گرامی هیچ پاسخی از سمت شما دریافت نشد.', 'danger')
        return redirect(url_for('fullstack_blueprint.course_content', course_id=course_id, item_id=item_id))

    @fullstack_blueprint.route('/my-courses')
    def my_courses():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        user_courses = user_courses_orm.User_courses.get_user_courses_by_user_id(user['id'])
        course = None
        if user_courses:
            for crs in user_courses:
                course = courses_orm.Courses.get_course_by_id(crs['course_id'])
                crs['title'] = course['title']
        return render_template('my-courses.html', user=user, courses = user_courses)
    
    @fullstack_blueprint.route('/my-items')
    def my_items():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        course_id = request.args.get('course_id')
        user_items = user_items_orm.User_items.get_all_user_items_by_ids(user['id'], course_id)
        for it in user_items:
            item = items_orm.Items.get_item_by_id(it['item_id'])
            it['title'] = item['title']
        return render_template('my-items.html', user=user, items = user_items, course_id=course_id)

    @fullstack_blueprint.route("/quiz-results/item_<item_id>")
    def user_quizzes(item_id):
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        user_quizzes = user_quizzes_orm.User_quizzes.get_all_user_quizzes_by_ids(user['id'], item_id)
        for quiz in user_quizzes:
            quiz['date'] = date_converter.Date_converter.unix_timestamp_to_jalali(quiz['unix_datetime'])
        return render_template('quiz_results.html', user=user, attender=user, user_quizzes=user_quizzes)

    