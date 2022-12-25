import jdatetime , json
from flask import redirect, render_template, request, session, url_for
from routes import common
from models_mysql import courses_orm, items_orm, quizzes_orm, questions_orm, comments_orm, course_news_orm, user_courses_orm, flash_messages_orm

flash_messages = []

def make_routes(goldis_blueprint):
    def listToString(list):
        string = ""
        for elemnt in list:
            string = elemnt + ',' + elemnt
        return string

    @goldis_blueprint.route("/course-info/course_<course_id>")
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
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(section_id)
        return render_template("course-info.html", course=course, all_courses_news=all_courses_news, user=user, all_comments=all_comments, flash_messages=flash_messages)

    @goldis_blueprint.route('/course-overview/course_<course_id>')
    def course_overview(course_id):
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

    @goldis_blueprint.route('/course-content/course_<course_id>/item_<item_id>')
    def course_content(course_id, item_id):
        user = common.get_user_from_token()
        user_course = user_courses_orm.User_courses.get_user_courses_by_item_id(item_id)
        if user_course:
            if user_course['item_id'] != int(item_id):
                jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
                jalali_time = jdatetime.datetime.now().strftime("%H:%M:%S")
                new_user_course_id = user_courses_orm.User_courses.insert_new_user_course(user_id = user['id'], jalali_date=jalali_date, jalali_time=jalali_time)
                update_user_course = user_courses_orm.User_courses.update_user_course(row_id=new_user_course_id, item_id=item_id )
        else:
            jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
            jalali_time = jdatetime.datetime.now().strftime("%H:%M:%S")
            new_user_course_id = user_courses_orm.User_courses.insert_new_user_course(user_id = user['id'], jalali_date=jalali_date, jalali_time=jalali_time)
            update_user_course = user_courses_orm.User_courses.update_user_course(row_id=new_user_course_id, item_id=item_id )
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
        quizzes = quizzes_orm.Quizzes.get_all_quizzes_with_questions(item_id)
        print(quizzes)
        if quizzes == []:
             quizzes = quizzes_orm.Quizzes.get_all_quizzes_by_item_id(item_id)
        all_comments = comments_orm.Comments.get_comments_by_section_id(
            f'course_content_{item_id}')
        last_comments = all_comments[0:19]
        return render_template("course-content.html", course=course, course_item=course_item, user=user, all_comments=last_comments, flash_messages=flash_messages, quizzes=quizzes)

    @goldis_blueprint.route("/quiz/quiz_<quiz_id>")
    def quiz_content(quiz_id):
        user = common.get_user_from_token()
        user_quiz = user_courses_orm.User_courses.get_user_quiz_by_quiz_id(quiz_id)
        jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
        jalali_time = jdatetime.datetime.now().strftime("%H:%M:%S")
        new_user_course_id = user_courses_orm.User_courses.insert_new_user_course(user_id=user['id'], jalali_date=jalali_date, jalali_time=jalali_time)
        update_user_quiz = user_courses_orm.User_courses.update_user_course(row_id=new_user_course_id, quiz_id=quiz_id)
        last_user_answers = []
        quizzes = quizzes_orm.Quizzes.get_all_quizzes()
        quiz = None
        for qz in quizzes:
            if str(qz['id']) == str(quiz_id):
                quiz = qz
                break
        questions = questions_orm.Questions.get_all_questions_by_ids(quiz_id)
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
        jalali_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
        jalali_time = jdatetime.datetime.now().strftime("%H:%M:%S")
        all_answers = request.form.get('all_answers')
        json_all_answers = json.loads(all_answers)
        string_all_answers = ','.join([str(elem) for i,elem in enumerate(json_all_answers)])
        new_user_result_id = user_courses_orm.User_courses.insert_new_user_course(user_id=user['id'], jalali_date=jalali_date, jalali_time=jalali_time)
        user_courses_orm.User_courses.update_user_course(row_id=new_user_result_id, quiz_id=quiz_id,user_answers=string_all_answers)
        return redirect(url_for('goldis_blueprint.course_content', course_id=course_id, item_id=item_id))

    @goldis_blueprint.route('/my-courses')
    def my_courses():
        user = common.get_user_from_token()
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(session['g_token'])
        user_courses = user_courses_orm.User_courses.get_user_courses_by_user_id(user['id'])
        return render_template('my-courses.html', user=user, courses = user_courses, flash_messages = flash_messages)

    @goldis_blueprint.route("/quiz-results/item_<item_id>")
    def user_quizzes(item_id):
        user = common.get_user_from_token()
        user_id = request.args.get('user_id')
        user_quizzes = user_courses_orm.User_courses.get_user_quizzes_by_item_id(item_id)
        return render_template('quiz_results.html', user=user, attender=user, user_quizzes=user_quizzes)

    