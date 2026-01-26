import os

class Config:
    # 格式: mysql+pymysql://用户名:密码@地址:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/flask_618_demo?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False