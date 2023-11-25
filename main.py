from app import create_app
from flask_cors import CORS
from app.extensions import start_socketio_run, init_db

from app.services.main.routes import main_bp
from app.services.auth.routes import auth_bp
from app.services.chat.routes import chat_bp
from app.services.test.routes import test_bp
from app.services.channels.routes import channels_bp
from app.services.user.routes import user_bp
from app.services.admin.routes import admin_bp

app = create_app()
# CORS(app)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(test_bp)
app.register_blueprint(channels_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    if not init_db(app):
        exit(0)

    start_socketio_run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
