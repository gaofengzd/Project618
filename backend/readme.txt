创建虚拟环境
python -m venv venv
激活虚拟环境
venv\Scripts\activate
安装包
pip install -r requirements.txt

backend/  # Flask 后端项目根目录
├── .env                # 全局环境变量（数据库配置、JWT 密钥、端口等）
├── .gitignore          # Git 忽略文件（venv、__pycache__、.pyc 等）
├── app.py              # 项目入口文件（创建 Flask 实例、注册蓝图、启动服务）
├── requirements.txt    # 项目依赖清单（记录所有安装的包，方便部署）
├── venv/               # Python 虚拟环境（无需提交 Git）
├── migrations/         # 数据库迁移文件（Flask-Migrate 生成，记录表结构修改）
├── instance/           # 实例目录（存储本地临时数据，如 SQLite 文件，可选）
└── app/                # 核心应用目录（开发重点关注，所有业务代码放在这里）
    ├── __init__.py     # 应用初始化文件（创建 Flask 实例、配置扩展、注册蓝图）
    ├── config.py       # 配置文件（加载环境变量、分环境配置开发/生产参数）
    ├── models/         # 数据模型目录（对应 MySQL 数据表，ORM 定义）
    │   ├── __init__.py # 导出模型类，方便其他模块导入
    │   ├── user.py     # 用户模型（对应 user 表）
    │   └── goods.py    # 商品模型（如有需要，按业务扩展）
    ├── api/            # 接口蓝图目录（按业务模块拆分，对应前端接口）
    │   ├── __init__.py # 蓝图注册统一管理
    │   ├── user.py     # 用户模块接口（登录、查询用户、修改信息等，蓝图）
    │   └── goods.py    # 商品模块接口（如有需要，按业务扩展）
    ├── services/       # 业务逻辑层目录（核心，封装复杂业务逻辑，解耦接口和模型）
    │   ├── __init__.py
    │   ├── user_service.py # 用户模块业务逻辑（如登录校验、密码加密、用户查询）
    │   └── goods_service.py # 商品模块业务逻辑
    ├── utils/          # 全局工具函数目录
    │   ├── __init__.py
    │   ├── jwt_utils.py # JWT 工具（生成 Token、验证 Token）
    │   ├── encrypt_utils.py # 加密工具（密码 bcrypt 加密、解密）
    │   └── response_utils.py # 响应格式封装（统一返回 JSON 格式，如成功/失败响应）
    └── extensions/     # 扩展插件初始化目录（统一管理 Flask 扩展，避免循环导入）
        ├── __init__.py
        ├── db.py        # SQLAlchemy 初始化
        ├── migrate.py   # Flask-Migrate 初始化
        └── jwt.py       # Flask-JWT-Extended 初始化