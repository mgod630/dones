from flask import redirect, render_template, request, url_for, session, jsonify
from routes import common
from models_mysql import courses_orm, course_news_orm, emails_orm, notifications_orm
import tools.date_converter as date_converter

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route("/")
    @fullstack_blueprint.route("/home")
    def home():
        section_id = 'home_page'
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        for course in all_courses:
            course['jalali_start_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(
                course['unix_start_datetime'])
            course['jalali_end_datetime'] = date_converter.Date_converter.unix_timestamp_to_jalali(
                course['unix_end_datetime'])
        all_courses_news = course_news_orm.Courses_news.get_courses_news_by_section_id(
            section_id)
        unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])
        if unread_notifications_count:
            unread_notifications_count = unread_notifications_count[0]
        return render_template("index.html", user=user, user_account=None, all_courses=all_courses, all_courses_news=all_courses_news, unread_notifications_count=unread_notifications_count)

    @fullstack_blueprint.route("/landing-page")
    def landing_page():
        user = common.get_user_from_token()
        return render_template('landing_page.html', user=user)

    @fullstack_blueprint.route("/landing-page-post", methods=['POST'])
    def landing_page_post():
        user = common.get_user_from_token()
        email = request.form.get('email')
        all_emails = emails_orm.Emails.get_all_emails()
        for eml in all_emails:
            if eml['email'] == email:
                result = 'email_already_exists'
                # return redirect(url_for('fullstack_blueprint.landing_page', result=result))
                # return jsonify({'result': result})
                # return render_template('landing_page.html', result=result)
                return {'result': result}
        try:
            new_user_email = emails_orm.Emails.insert_new_email(email)
            result = 'email_successfully_stored'
        except:
            result = 'something_went_wrong'
        # return redirect(url_for('fullstack_blueprint.landing_page', result=result))
        # return jsonify({'result': result})
        # return render_template('/landing_page.html', result=result)
        return {'result': result}

    @fullstack_blueprint.route("/404-not-found")
    def not_found():
        user = common.get_user_from_token()
        return render_template('404_not_found.html')
