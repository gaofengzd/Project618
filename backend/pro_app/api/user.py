from flask import Blueprint, jsonify, request
from pro_app.extensions.db import db
from pro_app.models.user import User

main_bp = Blueprint('api', __name__)

# 获取用户列表
@main_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
    # return jsonify([user.to_dict() for user in users])
        return "获取失"
    else:
        return jsonify(users)

# 添加新用户
@main_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201