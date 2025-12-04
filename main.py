from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from views import init_app

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    app.config['SECRET_KEY'] = "#TONOHUB"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Configura o login
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(Exception)
    def erro(e):
        code = getattr(e, "code", 404)
        mensagem = getattr(e, "description", str(e))
        return render_template("erro.html", codigo=code, mensagem=mensagem)

    return app


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)
