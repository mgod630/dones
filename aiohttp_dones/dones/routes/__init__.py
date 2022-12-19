from flask import Blueprint
from routes import account_routes, main_routes, user_routes, course_routes, comments_routes, dm_routes

def make_routes():
    goldis_blueprint = Blueprint('goldis_blueprint', __name__, template_folder='templates')
    main_routes.make_routes(goldis_blueprint)
    user_routes.make_routes(goldis_blueprint)
    account_routes.make_routes(goldis_blueprint)
    course_routes.make_routes(goldis_blueprint)
    comments_routes.make_routes(goldis_blueprint)
    dm_routes.make_routes(goldis_blueprint)
    return goldis_blueprint