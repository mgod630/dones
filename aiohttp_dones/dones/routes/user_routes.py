import secrets, time, random, sms
from flask import render_template, request, redirect, session, url_for, flash, current_app as app
from routes import common
from models_mysql import users_orm, accounts_orm, user_courses_orm

def make_routes(goldis_blueprint):
      
    @goldis_blueprint.route('/login')
    def login():
        return render_template('login.html', user=None)

    @goldis_blueprint.route('/login-post', methods=['POST'])
    def login_post():
        status = ''
        mobile = request.form.get('lg_mobile', None)
        error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
        password = request.form.get('lg_password', None)
        error, password = common.sanitize_user_input(common.User_post_data_types.Only_letter, password)
        user = users_orm.Users.get_user_by_mobile(mobile)
        if user != None:
            user = users_orm.Users.get_user_by_mobile_and_password(mobile, password)
            if user != None:
                session['g_token'] = user['g_token']
                return redirect(url_for('goldis_blueprint.home'))
            else :
                status = 'incorrect_password'
                return redirect(url_for('goldis_blueprint.login', status=status))
        else:
            status = 'user_not_found'
            return redirect(url_for('goldis_blueprint.login', status=status))
      
    @goldis_blueprint.route('/signup')
    def signup():
        return render_template('login.html', user=None)

    @goldis_blueprint.route('/signup-post', methods=['POST'])
    async def signup_post():
        step = request.args.get('step')
        if step == '1':
            mobile = request.form.get('sg_mobile', None)
            error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
            user = users_orm.Users.get_user_by_mobile(mobile)
            if user:
                status = 'mobile_already_exist'
                return redirect(url_for('goldis_blueprint.login', status=status))
            else:
                registering_code = random.randint(10000, 99999)
                response = await sms.send_message_by_313(mobile, str(registering_code))
                print(response)
                user_type = 0
                new_user_id = users_orm.Users.insert_new_user(mobile=mobile, user_type=user_type, register_datetime=time.time(), registering_code=registering_code)
                new_user = users_orm.Users.get_user_by_id(new_user_id)
                status = 'registering_code_sent'
                return redirect(url_for('goldis_blueprint.login', status=status))
        elif step == '2':
            registering_code = request.form.get('sg_registering_code')
            mobile = request.form.get('sg_mobile_step_2', None)
            error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
            user = users_orm.Users.get_user_by_mobile(mobile)
            if user['registering_code'] == registering_code:
                status = 'registering_code_correct'
                return redirect(url_for('goldis_blueprint.login', status=status))
            else:
                status = 'registering_code_incorrect'
                return redirect(url_for('goldis_blueprint.login', status=status))
        elif step == '3':
            mobile = request.form.get('sg_mobile_step_3', None)
            error, mobile = common.sanitize_user_input(common.User_post_data_types.mobile, mobile)
            full_name = request.form.get('sg_fullname', None)
            error, full_name = common.sanitize_user_input(common.User_post_data_types.Only_letter, full_name)
            password = request.form.get('sg_password', None)
            error, password = common.sanitize_user_input(common.User_post_data_types.Only_letter, password)
            g_token = secrets.token_hex()
            # user_type = users_orm.Users.Types.new_user
            new_user_id = users_orm.Users.update_user(id=id, full_name=full_name, g_token=g_token, password=password,register_datetime=time.time())
            session['g_token'] = g_token
            return redirect(url_for('goldis_blueprint.home'))

        return redirect(url_for('goldis_blueprint.login'))
    

    @goldis_blueprint.route('/logout')
    def logout():
        session.pop('g_token')
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/profile')
    def profile():
        user = common.get_user_from_token()
        if user == None:
            flash('برای ویرایش پروفایل ابتدا ثبت نام یا ورود نمایید.', 'danger')
            return redirect('/')
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
            return redirect(url_for('goldis_blueprint.profile'))
        else:
            mobile = request.form.get('sg_mobile', 'None')
            full_name = request.form.get('sg_fullname', 'None')
            update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name)
            flash(f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success')
            user = common.get_user_from_token()
            return redirect(url_for('goldis_blueprint.profile'))


