# 蓝图注册统一管理
from .user import main_bp
from .plane import plane_bp
from .init_db import init_bp

__all__ = ["main_bp", "plane_bp", "init_bp", ]