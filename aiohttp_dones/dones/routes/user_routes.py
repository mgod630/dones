import secrets, time
from flask import render_template, request, redirect, session, url_for, jsonify, g, current_app as app
from routes import common
from models_mysql import users_orm, accounts_orm, flash_messages_orm, user_courses_orm
status= ''
user= None 
flash_messages= None

def make_routes(goldis_blueprint):
      
    @goldis_blueprint.route('/login')
    def login():
        all_users = users_orm.Users.get_all_users()
        return render_template('login.html',status=status, user=None, flash_messages=flash_messages)

    @goldis_blueprint.route('/login-post', methods=['POST'])
    def login_post():
        status = ''
        mobile = request.form.get('lg_mobile', 'None')
        error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
        password = request.form.get('lg_password', 'None')
        error, password = common.sanitize_user_input(common.User_post_data_types.Only_letter, password)
        try:
            user = users_orm.Users.get_user_by_mobile_and_password(mobile, password)
            if user != None:
                session['g_token'] = user['g_token']
                return redirect(url_for('goldis_blueprint.home'))
            else :
                status = 'incorrect_password'
                return render_template('login.html',status=status, user=None, flash_messages=flash_messages)
        except TypeError:
            status = 'user_not_found'
            return render_template('login.html',status=status, user=None, flash_messages=flash_messages)
      
    @goldis_blueprint.route('/signup')
    def signup():
        return render_template('login.html',status=status, user=None, flash_messages=flash_messages)

    @goldis_blueprint.route('/signup-post', methods=['POST'])
    def signup_post():
        status = ''
        full_name = request.form.get('sg_fullname', 'None')
        error, full_name = common.sanitize_user_input(common.User_post_data_types.Only_letter, full_name)
        mobile = request.form.get('sg_mobile', 'None')
        error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
        password = request.form.get('sg_password', 'None')
        error, password = common.sanitize_user_input(common.User_post_data_types.Only_letter, password)
        g_token = secrets.token_hex()
        sheba_number = ''
        credit_score = 0
        user_type = users_orm.Users.Types.new_user
        invited_friend_mobile = ''
        try:
            new_user_id = users_orm.Users.insert_new_user(full_name, mobile, g_token, password, sheba_number, credit_score, user_type, invited_friend_mobile, time.time())
            new_user_account_id = accounts_orm.Accounts.insert_new_account(new_user_id, accounts_orm.Accounts.Types.A)
            session['g_token'] = g_token
        except :
            status = 'mobile_already_exist'
            return render_template('login.html',status=status, user=None, flash_messages=flash_messages)
        print(users_orm.Users.get_all_users())
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/logout')
    def logout():
        session.pop('g_token')
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/profile')
    def profile():
        user = common.get_user_from_token()
        flash_messages = flash_messages_orm.Flash_messages.get_flash_messages_by_user_token(session['g_token'])
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(session['g_token'])
        return render_template('profile.html', user=user, flash_messages= flash_messages)

    @goldis_blueprint.route('/profile', methods=['POST'])
    def profile_post():
        user = common.get_user_from_token()
        user_full_name = user['full_name']
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(session['g_token'])
        if request.form.get('sg_current_password') != 'None' and request.form.get('sg_new_password', 'None') != 'None':
            current_password = request.form.get('sg_current_password', 'None') 
            if common.check_password(current_password, user['password']) :
                new_password = request.form.get('sg_new_password', 'None')
                mobile = request.form.get('sg_mobile', 'None')
                full_name = request.form.get('sg_fullname', 'None')
                grade = request.form.get('grade', 'None')
                age = request.form.get('age', 'None')
                gender = request.form.get('gender', 'None')
                marital_status = request.form.get('marital_status', 'None')
                job = request.form.get('job', 'None')
                update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name, password=new_password, grade=grade, age=age, gender=gender, marital_status=marital_status, job=job)
                flash_messages_orm.Flash_messages.insert_new_flash_message(session['g_token'], f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success') 
            else:
                flash_messages_orm.Flash_messages.insert_new_flash_message(session['g_token'], f'{user_full_name} گرامی، رمز عبور فعلی، صحیح نمی باشد.', 'danger') 
            user = common.get_user_from_token()
            flash_messages = flash_messages_orm.Flash_messages.get_flash_messages_by_user_token(session['g_token'])
            return redirect('/profile')
        else:
            mobile = request.form.get('sg_mobile', 'None')
            full_name = request.form.get('sg_fullname', 'None')
            grade = request.form.get('grade', 'None')
            age = request.form.get('age', 'None')
            gender = request.form.get('gender', 'None')
            marital_status = request.form.get('marital_status', 'None')
            job = request.form.get('job', 'None')
            update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name, grade=grade, age=age, gender=gender, marital_status=marital_status, job=job)
            flash_messages_orm.Flash_messages.insert_new_flash_message(session['g_token'], f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success') 
            flash_messages = flash_messages_orm.Flash_messages.get_flash_messages_by_user_token(session['g_token'])
            user = common.get_user_from_token()
            return redirect('/profile')

    @goldis_blueprint.route('/my-courses')
    def my_courses():
        user = common.get_user_from_token()
        flash_messages_orm.Flash_messages.delete_flash_message_by_user_token(session['g_token'])
        user_courses = user_courses_orm.User_courses.get_user_courses_by_user_id(user['id'])
        return render_template('my-courses.html', user=user, courses = user_courses, flash_messages = flash_messages)


