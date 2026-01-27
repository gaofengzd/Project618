from pro_app import create_app
from pro_app.models.user import create_user_info

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
