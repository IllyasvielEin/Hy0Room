import logging
from flask import Flask
from app.extensions import init_all


def create_app():
    app = Flask(__name__)
    init_all(app)

    handler = app.logger.handlers[0]
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)

    class SocketIOFilter(logging.Filter):
        def filter(self, record):
            return "/socket.io/" not in record.getMessage()

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    # Apply the filter
    socket_io_filter = SocketIOFilter()
    log.addFilter(socket_io_filter)

    return app
