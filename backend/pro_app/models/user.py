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
        return f"<User(id={self.id}, username='{self.username}', age={self.age})>"\


def create_user_info(account, password, username, age, local):
    # 1. 先查询数据库中是否已存在该账号
    existing_user = User.query.filter_by(account=account).first()

    # 2. 如果存在，直接返回，不再执行后续插入操作
    if existing_user:
        print(f"账号 {account} 已存在，跳过初始化。")
        return
    # 方式1：创建单个用户
    user1 = User(
        account=account,
        password=password,
        username=username,
        age=age,
        local=local
    )
    # 添加到数据库会话（临时存储，未写入数据库）
    db.session.add(user1)

    # 提交会话（核心：真正写入数据库，必须执行）
    db.session.commit()
    print("数据新增成功！")
