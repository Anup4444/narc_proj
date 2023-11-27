from views.dashboards import dashboards
from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db
from views.auth import auth

import config
from models.user import User
from werkzeug.security import *
from flask_assets import Environment, Bundle
from blueprint.admin import admin_blueprint
from setup.appsetup import secret_key
from flask_mail import Mail
from extensions import mail
from config import Config


app = Flask(__name__)
app.config.from_object(config)
app.config.from_object(Config)
mail.init_app(app)

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['SECRET_KEY'] = secret_key


assets = Environment(app)
js = Bundle("js/Chart.min.js", output="gen/main.js")
assets.register("main_js", js)
# csrf.init_app(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
# Initialize mail with app
app.register_blueprint(auth)

app.register_blueprint(dashboards)
app.register_blueprint(admin_blueprint, url_prefix='/setup_form')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        superuser = User.query.filter_by(role='superuser').first()
        if not superuser:
            superuser = User(username='superuser', role='superuser')
            superuser.password = 'superpassword'
            db.session.add(superuser)
            db.session.commit()
    app.run(debug=True)
