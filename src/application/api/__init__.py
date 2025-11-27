from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from injector import Injector

from src import config
from src.application.api.controller import authentication_controller
from src.application.api.controller.authentication_controller import AuthenticationController
from src.application.api.controller.item_controller import ItemController
from src.application.api.controller.project_controller import ProjectController
from src.application.api.dependency_injector import DependencyInjector
from src.application.api.flask_alchemy_db_instance import FlaskAlchemyDBInstance
from src.application.api.register_controllers import instantiate_controllers
from src.application.api.security import authentication_utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.API_TOKEN_SECRET
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=config.API_TOKEN_EXPIRATION_HOURS)
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"

CORS(app)

db_instance = FlaskAlchemyDBInstance(app)
app_injector = Injector([DependencyInjector(app, db_instance)])

instantiate_controllers(app, app_injector)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
