# IMPORTS
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import setup_db, db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    migrate = Migrate(app, db)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # ENDPOINTS

    return app
