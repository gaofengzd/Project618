from flask import Blueprint, jsonify, request
from pro_app.extensions.db import db
from pro_app.models.user import User, create_user_info

main_bp = Blueprint('api', __name__)

# 获取用户列表
@main_bp.route('/users', methods=['GET'])
def get_users():
    # create_user_info(account='dsfds', password='123', username='张三', age=18, local='北京')
    # create_user_info(account='cxvcxzs', password='456', username='里斯', age=20, local='天津')
    users = User.query.all()
    if not users:
        return "获取失败"
    else:
        return jsonify([user.to_dict() for user in users])

# 添加新用户
@main_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201