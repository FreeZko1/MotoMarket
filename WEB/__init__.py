from flask import Flask
from DB.database_connection import DatabaseConnection
from flask import Flask
from DB.database_connection import DatabaseConnection
from .auth import auth
from .vehicles import vehicles as vehicles_blueprint
from .user_profiles import user_profiles
from .news import news as news_blueprint
from .compare_vehicles import compare as compare_blueprint
from .chat import chat as chat_blueprint
from .quiz import quiz_blueprint
from .adminfeatures import admin


def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = "honza"
    

    
    database_connection = DatabaseConnection()

    app.db_connection = database_connection.connect()

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    from .vehicles import vehicles as vehicles_blueprint
    app.register_blueprint(vehicles_blueprint)

    from .user_profiles import user_profiles
    app.register_blueprint(user_profiles, url_prefix='/user')

    from .news import news as news_blueprint
    app.register_blueprint(news_blueprint)

    from .compare_vehicles import compare
    app.register_blueprint(compare, url_prefix='/compare')

    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    from .quiz import quiz_blueprint
    app.register_blueprint(quiz_blueprint)

    from .adminfeatures import admin
    app.register_blueprint(admin, url_prefix='/admin')

   

    return app


