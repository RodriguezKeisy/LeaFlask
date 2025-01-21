import os
import warnings

from flask import Flask
from flask_migrate import Migrate
from models.conn import db
from flask_login import LoginManager
from blueprints.auth import auth as auth_blueprint
from dotenv import load_dotenv
from blueprints.image import image_bp

from models.models import User
from blueprints.hello import hello


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)
warnings.simplefilter(action='ignore', category=FutureWarning)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(image_bp)
app.register_blueprint(hello)

@login_manager.user_loader
def load_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user

if __name__ == '__main__':
    app.run(debug=os.getenv('APP_TEST', False))
