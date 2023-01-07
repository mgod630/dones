import secrets, time, random, tools.sms as sms
from flask import render_template, request, redirect, session, url_for, flash, current_app as app
from routes import common
from models_mysql import users_orm

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route('/login')
    def login():
        return render_template('login.html', user=None)

    @fullstack_blueprint.route('/login-post', methods=['POST'])
    def login_post():
        status = ''
        mobile = request.form.get('lg_mobile', None)
        password = request.form.get('lg_password', None)
        user = users_orm.Users.get_user_by_mobile(mobile)
        if user != None:
            user = users_orm.Users.get_user_by_mobile_and_password(mobile, password)
            if user != None:
                session['g_token'] = user['g_token']
                return redirect(url_for('fullstack_blueprint.home'))
            else :
                status = 'incorrect_password'
                return redirect(url_for('fullstack_blueprint.login', status=status))
        else:
            status = 'user_not_found'
            return redirect(url_for('fullstack_blueprint.login', status=status))
      
    @fullstack_blueprint.route('/signup')
    def signup():
        return render_template('login.html', user=None)

    @fullstack_blueprint.route('/signup-post', methods=['POST'])
    async def signup_post():
        step = request.args.get('step')
        if step == '1':
            if 'mobile' in session:
                session.pop('mobile', None)
            mobile = request.form.get('sg_mobile', None)
            user = users_orm.Users.get_user_by_mobile(mobile)
            if user and (user['user_type'] in (users_orm.Users.Types.system_user.value, users_orm.Users.Types.admin.value, users_orm.Users.Types.super_admin.value)):
                status = 'mobile_already_exist'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            elif user and user['user_type'] == users_orm.Users.Types.unregistered_user.value :
                registering_code = random.randint(10000, 99999)
                await sms.send_message_by_313(mobile, str(registering_code))
                session['mobile'] = mobile
                update_unregistered_user = users_orm.Users.update_user_by_mobile(mobile=mobile, register_datetime=time.time(), registering_code=registering_code)
                status = 'registering_code_sent'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            elif user and user['user_type'] == users_orm.Users.Types.registered_user.value :
                if user['register_datetime'] - time.time() > 86400 : # after one day
                    registering_code = random.randint(10000, 99999)
                    await sms.send_message_by_313(mobile, str(registering_code))
                    session['mobile'] = mobile
                    update_registered_user = users_orm.Users.update_user_by_mobile(mobile=mobile, register_datetime=time.time(), registering_code=registering_code)
                    status = 'registering_code_sent'
                    return redirect(url_for('fullstack_blueprint.login', status=status))
                else:
                    status = 'registering_code_correct'
                    return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                registering_code = random.randint(10000, 99999)
                await sms.send_message_by_313(mobile, str(registering_code))
                user_type = users_orm.Users.Types.unregistered_user.value
                g_token = secrets.token_hex()
                session['mobile'] = mobile
                unregistered_user = users_orm.Users.insert_new_user(mobile=mobile, user_type=user_type, g_token=g_token, register_datetime=time.time(), registering_code=registering_code)
                status = 'registering_code_sent'
                return redirect(url_for('fullstack_blueprint.login', status=status))
        elif step == '2' :
            if 'mobile' not in session:
                status = 'mobile_is_not_entered'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            registering_code = request.form.get('registering_code')
            user = users_orm.Users.get_user_by_mobile(session['mobile'])
            if str(user['registering_code']) == registering_code:
                user_type = user_type = users_orm.Users.Types.registered_user.value
                registered_user = users_orm.Users.update_user_by_mobile(mobile=session['mobile'], user_type=user_type)
                status = 'registering_code_correct'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                status = 'registering_code_incorrect'
                return redirect(url_for('fullstack_blueprint.login', status=status))
        elif step == '3':
            if 'mobile' not in session:
                status = 'mobile_is_not_entered'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                user = users_orm.Users.get_user_by_mobile(session['mobile'])
                if user and  user['user_type'] == users_orm.Users.Types.registered_user.value:
                    full_name = request.form.get('sg_fullname', None)
                    password = request.form.get('sg_password', None)
                    g_token = secrets.token_hex()
                    user_type = users_orm.Users.Types.system_user.value
                    new_user_id = users_orm.Users.update_user_by_mobile(mobile=session['mobile'], full_name=full_name, user_type=user_type, g_token=g_token, password=password, register_datetime=time.time())
                    if 'mobile' in session:
                        session.pop('mobile', None)
                    session['g_token'] = g_token
                    return redirect(url_for('fullstack_blueprint.home'))
                else :
                    status = 'user_is_not_registered'
                    return redirect(url_for('fullstack_blueprint.login', status=status))
        if 'mobile' not in session:
            status = 'mobile_is_not_entered'
            return redirect(url_for('fullstack_blueprint.login', status=status))
        return redirect(url_for('fullstack_blueprint.login'))

    @fullstack_blueprint.route('/reset-password', methods=['POST'])
    async def reset_password():
        step = request.args.get('step')
        if step == '1':
            if 'mobile' in session:
                session.pop('mobile', None)
            mobile = request.form.get('rp_mobile', None)
            user = users_orm.Users.get_user_by_mobile(mobile)
            if user == None:
                status = 'user_not_found'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            if user and (user['user_type'] in (users_orm.Users.Types.system_user.value, users_orm.Users.Types.admin.value, users_orm.Users.Types.super_admin.value)):
                registering_code = random.randint(10000, 99999)
                await sms.send_message_by_313(mobile, str(registering_code))
                session['mobile'] = mobile
                users_orm.Users.update_user_by_mobile(mobile=mobile, registering_code=registering_code)
                status = 'rp_registering_code_sent'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                status = 'user_is_not_registered'
                return redirect(url_for('fullstack_blueprint.login', status=status))
        elif step == '2' :
            if 'mobile' not in session:
                status = 'rp_mobile_is_not_entered'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            registering_code = request.form.get('rp_registering_code')
            user = users_orm.Users.get_user_by_mobile(session['mobile'])
            if str(user['registering_code']) == registering_code:
                status = 'rp_registering_code_correct'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                status = 'rp_registering_code_incorrect'
                return redirect(url_for('fullstack_blueprint.login', status=status))
        elif step == '3':
            if 'mobile' not in session:
                status = 'rp_mobile_is_not_entered'
                return redirect(url_for('fullstack_blueprint.login', status=status))
            else:
                user = users_orm.Users.get_user_by_mobile(session['mobile'])
                if user and  user['user_type'] == users_orm.Users.Types.registered_user.value:
                    password = request.form.get('rp_password', None)
                    update_user_password = users_orm.Users.update_user_by_mobile(mobile=session['mobile'], password=password)
                    if 'mobile' in session:
                        session.pop('mobile', None)
                    # session['g_token'] = user['g_token']
                    return redirect(url_for('fullstack_blueprint.home'))
                else :
                    status = 'user_is_not_registered'
                    return redirect(url_for('fullstack_blueprint.login', status=status))
        if 'mobile' not in session:
            status = 'rp_mobile_is_not_entered'
            return redirect(url_for('fullstack_blueprint.login', status=status))
        return redirect(url_for('fullstack_blueprint.login'))
    
    @fullstack_blueprint.route('/logout')
    def logout():
        session.pop('g_token')
        return redirect(url_for('fullstack_blueprint.home'))

    @fullstack_blueprint.route('/profile')
    def profile():
        user = common.get_user_from_token()
        if user == None:
            flash('برای ویرایش پروفایل ابتدا ثبت نام یا ورود نمایید.', 'danger')
            return redirect('/')
        return render_template('profile.html', user=user)

    @fullstack_blueprint.route('/profile', methods=['POST'])
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
            return redirect(url_for('fullstack_blueprint.profile'))
        else:
            mobile = request.form.get('sg_mobile', 'None')
            full_name = request.form.get('sg_fullname', 'None')
            update_user = users_orm.Users.update_user(id=user['id'], mobile=mobile, full_name=full_name)
            flash(f'{user_full_name} گرامی پروفایل شما با موفقیت ویرایش گردید.', 'success')
            user = common.get_user_from_token()
            return redirect(url_for('fullstack_blueprint.profile'))


