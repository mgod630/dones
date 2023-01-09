from flask import Blueprint
from routes import account_routes, main_routes, user_routes, course_routes, comments_routes, dm_routes, transaction_routes, notifications_routes

def make_routes():
    fullstack_blueprint = Blueprint('fullstack_blueprint', __name__, template_folder='templates')
    main_routes.make_routes(fullstack_blueprint)
    user_routes.make_routes(fullstack_blueprint)
    account_routes.make_routes(fullstack_blueprint)
    course_routes.make_routes(fullstack_blueprint)
    comments_routes.make_routes(fullstack_blueprint)
    dm_routes.make_routes(fullstack_blueprint)
    transaction_routes.make_routes(fullstack_blueprint)
    notifications_routes.make_routes(fullstack_blueprint)
    return fullstack_blueprint