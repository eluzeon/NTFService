from app import create_app
from app.configs import Dev


if __name__ == '__main__':
    app = create_app(Dev)
    app.run()
