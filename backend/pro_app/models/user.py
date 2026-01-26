from pro_app.extensions.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID（主键）')
    account = db.Column(db.String(100), unique=True, nullable=False, comment='用户账户')
    password = db.Column(db.String(100), nullable=False, comment='用户密码')
    username = db.Column(db.String(50), nullable=False, comment='用户名字')
    age = db.Column(db.Integer, nullable=False, comment='用户年龄')
    local = db.Column(db.String(50),  nullable=False, comment='用户所在地')

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'age': self.age
    #     }
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', age={self.age})>"