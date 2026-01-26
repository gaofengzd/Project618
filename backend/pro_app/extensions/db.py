# SQLAlchemy 初始化
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
# 允许跨域请求，这对于前后端分离至关重要
cors = CORS()