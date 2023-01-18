import os
import secrets
from flask import Flask, request, redirect
import mysql.connector.pooling
from routes import make_routes, common

def init(config_file="settings.py"):
    app = Flask(__name__)          
    app.config.from_pyfile(config_file)
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploaded_files")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
    app.config["SECRET_KEY"] = 'secrets.token_hex(16)'
    # TODO Use pure in production
    app.config['mysql_connection_pool'] = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='full_stack', use_pure=True, pool_name="my_pool", pool_size=32, buffered=True)
    no_login_need_urls = ["/login", "/login-post", "/signup", "/signup-post"]
    fullstack_blueprint = make_routes()
    app.register_blueprint(fullstack_blueprint)

    @app.before_request
    def before_request_func():
        # new_response = redirect('/login')d
        new_response = None
        if request.path in no_login_need_urls or common.get_user_from_token() != None:
            new_response = None
        return new_response
    return app


if __name__ == "__main__" and True:
    app = init()
    app.run(port=5002)
