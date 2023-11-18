import logging
from flask import Flask
from app.extensions import init_all

def create_app():
    app = Flask(__name__)
    init_all(app)

    handler = app.logger.handlers[0]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    return app
