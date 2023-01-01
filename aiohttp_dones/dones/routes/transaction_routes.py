import zarinpal 
from flask import redirect, render_template, request, session, url_for, flash
from routes import common
from models_mysql import user_courses_orm ,user_quizzes_orm, user_items_orm

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route("/token-buy-invoice")
    def token_buy_invoice():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        course_id = request.args.get('course_id')
        error, ipg_url, ipg_ref_id = zarinpal.zarinpal_make_payment('09035214248',5000)
        return redirect(f'{ipg_url}')

    @fullstack_blueprint.route("/zarinpal-callback")
    def zarinpal_callback():
        transaction = {}
        error = None
        course_id = 3
        ipg_ref_id = request.args.get('Authority', None)
        if request.args.get('Status') == 'OK':
            status = 'Transaction was successful'
            transaction['ipg_ref_id'] = ipg_ref_id
            transaction['amount'] = 5000
            error = zarinpal.verify_zarinpal_payment_transaction(transaction)
        else:
            error = 'Transaction failed or canceled by user'
        return redirect(url_for('fullstack_blueprint.course_overview', course_id=course_id, error=error))