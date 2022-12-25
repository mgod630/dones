from flask import redirect, render_template, request, url_for
from routes import common
from models_mysql import  courses_orm, course_news_orm, notices_orm, emails_orm


def make_routes(goldis_blueprint):
    @goldis_blueprint.route("/")
    @goldis_blueprint.route("/home")
    def home():
        flash_messages = []
        db_number = 1
        user = common.get_user_from_token()
        all_courses = courses_orm.Courses.get_all_courses()
        section_id = '0'
        all_course_news = course_news_orm.Courses_news.get_courses_news_by_section_id(section_id)
        return render_template("index.html", user=user, user_account=None, all_courses=all_courses, all_course_news=all_course_news, flash_messages=flash_messages, db_number=db_number)

    @goldis_blueprint.route("/landing-page")
    def landing_page():
        user = common.get_user_from_token()
        return render_template('landing_page.html', user=user)

    @goldis_blueprint.route("/landing-page-post", methods=['POST'])
    def landing_page_post():
        user = common.get_user_from_token()
        email = request.form.get('email')
        all_emails = emails_orm.Emails.get_all_emails()
        for eml in all_emails:
            if eml['email'] ==  email:
                result = 'email_already_exists'
                return redirect(url_for('goldis_blueprint.landing_page', result=result))
        try:
            new_user_email = emails_orm.Emails.insert_new_email(email)
            result = 'email_successfully_stored'
        except: 
            result = 'something_went_wrong'
        return redirect(url_for('goldis_blueprint.landing_page', result=result))

    @goldis_blueprint.route("/404-not-found")
    def not_found():
        user = common.get_user_from_token()
        return render_template('404_not_found.html')
