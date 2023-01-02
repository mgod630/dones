import zarinpal, time
from flask import redirect, render_template, request, session, url_for, flash
from routes import common
from models_mysql import transactions_orm , courses_orm, user_items_orm

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route("/token-buy-invoice")
    def token_buy_invoice():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        user_full_name = user['full_name']
        course_id = request.args.get('course_id')
        course = courses_orm.Courses.get_course_by_id(course_id)
        amount = course['price']
        error, ipg_url, ipg_ref_id = zarinpal.zarinpal_make_payment(user['mobile'], amount)
        if error:
            transaction_status = transactions_orm.Transactions.Status.failed.value
            transaction_type = transactions_orm.Transactions.Types.buy_token.value
            description = ''
            transaction = transactions_orm.Transactions.insert_new_transaction(user_id=user['id'], course_id=course_id, ipg_ref_id=ipg_ref_id, amount=amount, transaction_type=transaction_type, transaction_status=transaction_status, description=description)
            flash(f'{user_full_name} گرامی، با عرض پوزش در هنگام اتصال به درگاه بانک خطایی رخ داده است.', 'danger')
            return redirect(url_for('fullstack_blueprint.course_overview', course_id=course_id))
        session['ipg_url'] = ipg_url
        transaction_status = transactions_orm.Transactions.Status.Unknown.value
        transaction_type = transactions_orm.Transactions.Types.buy_token.value
        description = ''
        transaction = transactions_orm.Transactions.insert_new_transaction(user_id=user['id'], course_id=course_id, ipg_ref_id=ipg_ref_id, amount=amount, transaction_type=transaction_type, status=transaction_status, create_datetime=time.time(), description=description)
        return render_template('token_buy_invoice.html', course_id=course_id, user=user, transaction=transaction)

    @fullstack_blueprint.route("/token-buy-invoice", methods=['POST'])
    def token_buy_invoice_post():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        course_id = request.args.get('course_id')
        ipg_url = session['ipg_url']
        return redirect(f'{ipg_url}')
        # return render_template('token_buy_invoice.html', course_id=course_id, user=user)

    @fullstack_blueprint.route("/bill-result")
    def bill_result():
        invoice_result = None
        if request.args.get('invoice_number') :
            ipg_ref_id = request.args.get('invoice_number')
            transaction = transactions_orm.Transactions.get_transaction_by_ipg_id(ipg_ref_id)
            if transaction:
                invoice_result = transaction
        if invoice_result == None:
            return redirect(url_for('fullstack_blueprint.home'))
        return render_template('bill_result.html', invoice_result=invoice_result)

    @fullstack_blueprint.route("/zarinpal-callback")
    def zarinpal_callback():
        if 'ipg_url' in session:
            session.pop('ipg_url', None)
        error = None
        ipg_ref_id = request.args.get('Authority', None)
        if request.args.get('Status') == 'OK':
            transaction = transactions_orm.Transactions.get_transaction_by_ipg_id(ipg_ref_id)
            if transaction:
                result = zarinpal.verify_zarinpal_payment_transaction(transaction)
                if result.Status == 100: #str(result.RefID)
                    error = None
                    ipg_payment_id = result.RefID
                    transaction_status = transactions_orm.Transactions.Status.successful.value
                    description = 'Transaction successful'
                    update_transaction = transactions_orm.Transactions.update_transaction_by_ipg_id(ipg_ref_id=ipg_ref_id, status=transaction_status, ipg_payment_id=ipg_payment_id, description=description)
                elif result.Status== 101:
                    error = 'Transaction submitted : ' + str(result.Status)
                else:
                    error, description = 'Transaction failed. Status: ' + str(result.Status)
                    transaction_status = transactions_orm.Transactions.Status.failed.value
                    update_transaction = transactions_orm.Transactions.update_transaction_by_ipg_id(ipg_ref_id=ipg_ref_id, status=transaction_status, description=description)
        else:
            error = 'Transaction failed or canceled by user'
            transaction_status = transactions_orm.Transactions.Status.canceled.value
            description = 'Transaction failed or canceled by user'
            update_transaction = transactions_orm.Transactions.update_transaction_by_ipg_id(ipg_ref_id=ipg_ref_id, status=transaction_status, description=description)
        return redirect(url_for('fullstack_blueprint.bill_result', invoice_number=ipg_ref_id))

        