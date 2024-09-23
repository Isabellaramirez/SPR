from flask import Flask
import pymysql.cursors
from config import Config 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )


    from app.controllers.user_controller import user_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.pres_controller import pres_bp
    from app.controllers.contra_controller import contra_bp


    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(contra_bp)
    app.register_blueprint(pres_bp)

    app.connection = connection 

    return app

