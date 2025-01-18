from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Crea y configura una instancia de la aplicación Flask.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)

    return app
