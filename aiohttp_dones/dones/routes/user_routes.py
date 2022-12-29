import secrets, time
from flask import render_template, request, redirect, session, url_for, flash, current_app as app
from routes import common
from models_mysql import users_orm, accounts_orm, flash_messages_orm, user_courses_orm

def make_routes(goldis_blueprint):
      
    @goldis_blueprint.route('/login')
    def login():
        all_users = users_orm.Users.get_all_users()
        return render_template('login.html', user=None)

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
                return render_template('login.html',status=status, user=None)
        except TypeError:
            status = 'user_not_found'
            return render_template('login.html',status=status, user=None)
      
    @goldis_blueprint.route('/signup')
    def signup():
        return render_template('login.html', user=None)

    @goldis_blueprint.route('/signup-post', methods=['POST'])
    def signup_post():
        status = ''
        full_name = request.form.get('sg_fullname', 'None')
        error, full_name = common.sanitize_user_input(common.User_post_data_types.Only_letter, full_name)
        mobile = request.form.get('sg_mobile', 'None')
        error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
        password = request.form.get('sg_password', 'None')
        error, password = common.sanitize_user_input(common.User_post_data_types.Only_letter, password)
        registering_code = 0
        g_token = secrets.token_hex()
        # user_type = users_orm.Users.Types.new_user
        user_type = 0
        user = users_orm.Users.get_user_by_mobile(mobile)
        if user:
            status = 'mobile_already_exist'
            return render_template('login.html',status=status, user=None)
        else :
            new_user_id = users_orm.Users.insert_new_user(full_name, mobile, g_token, password, user_type, time.time(), registering_code)
            new_user_account_id = accounts_orm.Accounts.insert_new_account(new_user_id, accounts_orm.Accounts.Types.A)
            session['g_token'] = g_token   
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/logout')
    def logout():
        session.pop('g_token')
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/profile')
    def profile():
        user = common.get_user_from_token()
        return render_template('profile.html', user=user)

    @goldis_blueprint.route('/profile', methods=['POST'])
    def profile_post():
        user = common.get_user_from_token()
        user_full_name = user['full_name']
        if request.form.get('sg_current_password') != 'None' and request.form.get('sg_new_password', 'None') != 'None':
            current_password = request.form.get('sg_current_password', 'None') 
            if common.check_password(current_password, user['password']) :
                new_password = request.form.get('sg_new_password', 'None')
                mobile = request.form.get('sg_mobile', 'None')
                full_name = request.form.get('sg_fullname', 'None')
                update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name, password=new_password)
                flash(f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success')
            else:
                flash(f'{user_full_name} گرامی، رمز عبور فعلی، صحیح نمی باشد.', 'danger')
            user = common.get_user_from_token()
            return redirect('/profile')
        else:
            mobile = request.form.get('sg_mobile', 'None')
            full_name = request.form.get('sg_fullname', 'None')
            update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name)
            flash(f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success')
            user = common.get_user_from_token()
            return redirect('/profile')


