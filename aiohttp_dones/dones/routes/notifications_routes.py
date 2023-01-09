from flask import redirect, render_template, request, url_for
from models_mysql import course_news_orm, comments_orm
from routes import common
import time
from tools import date_converter

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route('/notifications')
    def notifications():
      return render_template('notifications.html')