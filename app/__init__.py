from flask import Flask
from flask_jwt_extended import JWTManager
from os import getenv

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = getenv("SECRET_KEY")

    jwt.init_app(app)

    from .auth import auth_blueprint
    from .organisations import org_blueprint
    from .home import home_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(org_blueprint, url_prefix='/api')
    app.register_blueprint(home_blueprint)

    return app
