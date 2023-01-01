import time
from flask import redirect, render_template, request, session, url_for, jsonify
from routes import common
from models_mysql import assets_orm, transactions_orm, accounts_orm


def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route("/trade-gold")
    def trade_gold():
        user = common.get_user_from_token()
        gold_asset = assets_orm.Assets.get_asset_by_code('GOLD')
        return render_template("trade_gold.html", user=user, gold_asset=gold_asset)

    @fullstack_blueprint.route('/buy-gold-post', methods=['POST'])
    def buy_gold_post():
        redirect_address = '/trade-gold'
        gold_amount = request.form.get('gold_amount', 'None')
        error, gold_amount = common.sanitize_user_input(
            common.User_post_data_types.Only_number, gold_amount)
        user = common.get_user_from_token()
        user_account = accounts_orm.Accounts.get_account_by_user_id(user['id'])
        gold_asset = assets_orm.Assets.get_asset_by_code('GOLD')
        rial_amount = gold_amount * gold_asset['buy_price']
        create_datetime = time.time()
        status = transactions_orm.Transactions.Status.pending
        if gold_amount > 0 and rial_amount <= user_account['rial_balance']:
            transaction_type = transactions_orm.Transactions.Types.buy_token
            new_transaction_id = transactions_orm.Transactions.insert_new_transaction(user_account['id'], gold_asset['id'], gold_amount,
                                                                                      create_datetime, transaction_type, status, gold_asset['buy_price'], 'Buy Gold.')
            redirect_address = f'/invoice?transaction_id={new_transaction_id}'
        elif gold_amount < 0 and user_account['gold_18k_balance'] >= gold_amount * -1:
            gold_amount *= -1
            transaction_type = transactions_orm.Transactions.Types.sell_token
            new_transaction_id = transactions_orm.Transactions.insert_new_transaction(user_account['id'], gold_asset['id'], gold_amount,
                                                                                      create_datetime, transaction_type, status, gold_asset['sell_price'], 'Sell Gold.')
            redirect_address = f'/invoice?transaction_id={new_transaction_id}'
        return redirect(redirect_address)

    @fullstack_blueprint.route('/sell-gold-post', methods=['POST'])
    def sell_gold_post():
        redirect_address = '/trade-gold'
        gold_amount = request.form.get('gold_amount', 'None')
        error, gold_amount = common.sanitize_user_input(
            common.User_post_data_types.Only_number, gold_amount)
        user = common.get_user_from_token()
        user_account = accounts_orm.Accounts.get_account_by_user_id(user['id'])
        gold_asset = assets_orm.Assets.get_asset_by_code('GOLD')
        if user_account['gold_18k_balance'] >= gold_amount:
            create_datetime = time.time()
            transaction_type = transactions_orm.Transactions.Types.sell_token
            status = transactions_orm.Transactions.Status.pending
            new_transaction_id = transactions_orm.Transactions.insert_new_transaction(user_account['id'], gold_asset['id'], gold_amount,
                                                                                      create_datetime, transaction_type, status, gold_asset['sell_price'], 'Sell Gold.')
            redirect_address = f'/invoice?transaction_id={new_transaction_id}'
        return redirect(redirect_address)

    @fullstack_blueprint.route("/invoice")
    def invoice():
        transaction_id = request.args.get('transaction_id', None)
        error, transaction_id = common.sanitize_user_input(
            common.User_post_data_types.Only_number, transaction_id)
        transaction = transactions_orm.Transactions.get_transaction_by_id(
            transaction_id)
        gold_asset = assets_orm.Assets.get_asset_by_code('GOLD')
        user = common.get_user_from_token()
        user_account = accounts_orm.Accounts.get_account_by_user_id(user['id'])
        return render_template("invoice.html", user=user, user_account=user_account, gold_asset=gold_asset, transaction=transaction)

    @fullstack_blueprint.route('/invoice-post', methods=['POST'])
    def invoice_post():
        transaction_id = request.args.get('transaction_id', None)
        error, transaction_id = common.sanitize_user_input(
            common.User_post_data_types.Only_number, transaction_id)
        transaction = transactions_orm.Transactions.get_transaction_by_id(
            transaction_id)
        gold_asset = assets_orm.Assets.get_asset_by_code('GOLD')
        user = common.get_user_from_token()
        user_account = accounts_orm.Accounts.get_account_by_user_id(user['id'])
        rial_amount = transaction['amount'] * \
            transaction['asset_price_at_transaction_time']
        if transaction['amount'] > 0 and ((transaction['transaction_type'] == transactions_orm.Transactions.Types.buy_token.value and user_account['rial_balance'] >= rial_amount) or (transaction['transaction_type'] == transactions_orm.Transactions.Types.sell_token.value and user_account['gold_18k_balance'] >= transaction['amount'])):
            accounts_orm.Accounts.buy_or_sell_gold_transaction(transaction_id)
        return redirect('/home')
