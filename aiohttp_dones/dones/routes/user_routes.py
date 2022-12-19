import secrets, time
from flask import render_template, request, redirect, session, url_for, jsonify, g, current_app as app
from routes import common
from models_mysql import users_orm, accounts_orm
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
                status = 'user_not_found'
                return render_template('login.html',status=status, user=None, flash_messages=flash_messages)
        except TypeError:
            print('TypeError')
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
            print('mobile_already_exist')
            return render_template('login.html',status=status, user=None, flash_messages=flash_messages)
        # test
        # users_orm.Users.delete_all_users()
        print(users_orm.Users.get_all_users())
        return redirect(url_for('goldis_blueprint.home'))

    @goldis_blueprint.route('/logout')
    def logout():
        session.pop('g_token')
        return redirect(url_for('goldis_blueprint.home'))
