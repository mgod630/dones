import enum
from flask import make_response, request, session
import bcrypt
from models_mysql import users_orm, transactions_orm, user_items_orm


def get_user_from_token():
    user = None
    if 'g_token' in session:
        user = users_orm.Users.get_user_by_g_token(session['g_token'])
    return user

def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf8'), hashed_password.encode('utf8'))

class User_post_data_types(enum.Enum):
    Only_number = enum.auto()
    mobile = enum.auto()
    Only_letter = enum.auto()
    Only_letter_and_number = enum.auto()

class Errors(enum.IntEnum):
    no_error = 1
    unknown_error = 2
    mobile_not_found = 3
    password_is_incorrect = 4
    maximum_asset_buy_limit_exceeded = 5
    maximum_asset_sell_limit_exceeded = 6
    login_required = 7
    data_is_invalid = 8

def sanitize_user_input(data_type, data):
    sanitized_data = error = None
    if data_type == User_post_data_types.Only_number:
        try:
            sanitized_data = int(data)
        except:
            try:
                sanitized_data = float(data)
            except:
                pass
        if sanitized_data == None:
            error = Errors.data_is_invalid
    elif data_type == User_post_data_types.mobile:
        try:
            sanitized_data = f'0{int(data)}'
        except:
            error = Errors.data_is_invalid
    elif data_type == User_post_data_types.Only_letter:
        sanitized_data = data.replace('"','').replace("'",'').replace('`','').replace(',','').replace(';','')
    return error, sanitized_data

def create_invoice_number() :
    invoice_number = None
    # last_rowid = user_items_orm.User_items.get_last_rowid()
    last_rowid = transactions_orm.Transactions.get_last_rowid()
    if last_rowid:
        next_transaction_number = last_rowid['id'] + 1
        invoice_number = f'fs{"0" * (16 - len(str(next_transaction_number)))}{next_transaction_number}'
    else:
        next_transaction_number = 1
        invoice_number = f'fs{"0" * (16 - len(str(next_transaction_number)))}{next_transaction_number}'
    return invoice_number
