from flask import Flask
from DB.database_connection import DatabaseConnection
from flask import Flask
from DB.database_connection import DatabaseConnection


def create_app():
    # Vytvoření nové instance webové aplikace.
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = "honza"
    

    
    database_connection = DatabaseConnection()

    app.db_connection = database_connection.connect()


    #Import a registrace modulů
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

    from .faq import faq
    app.register_blueprint(faq)

    from .ads import ads_bp
    app.register_blueprint(ads_bp)


    return app


