from flask import Flask
from pro_app.config import Config
from pro_app.api import *
from pro_app.extensions.db import db, cors
from pro_app.extensions.jwt import jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(plane_bp)
    app.register_blueprint(init_bp)

    # 创建数据库表（仅用于开发环境）
    with app.app_context():
        db.create_all()

    return app
