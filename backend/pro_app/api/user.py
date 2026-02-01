from flask import Blueprint, jsonify, request
from pro_app.extensions.db import db
from pro_app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

main_bp = Blueprint('login', __name__)

# === 路由: 登录 ===
@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 1. 查找用户
    user = User.query.filter_by(username=username).first()

    # 2. 验证密码
    if user and check_password_hash(user.password_hash, password):
        # 3. 生成 Token
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'token': access_token,
                'userInfo': {
                    'username': user.username,
                    'role': user.role
                }
            }
        }), 200
    else:
        return jsonify({'code': 401, 'msg': '用户名和密码错误'}), 401

