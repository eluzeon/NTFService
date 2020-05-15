from typing import Type, Union

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_marshmallow import Marshmallow
from flask_restful import Api

from app.models import db
from app.routes import NotificationResource
from app.configs import Dev, DefaultConfig


csrf_protect = CSRFProtect()
marsh = Marshmallow()


def set_api():
    api = Api(decorators=[csrf_protect.exempt])
    api.add_resource(NotificationResource, '/notifications')
    return api


APPS = [
    csrf_protect,
    set_api(),
    marsh,
    db
]


def create_app(cfg: Union[Type[DefaultConfig], DefaultConfig] = Dev):
    app = Flask(__name__)
    app.config.from_object(cfg)
    for _app in APPS:
        _app.init_app(app)
    return app
