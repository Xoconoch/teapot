from dotenv import load_dotenv
import os
from app import create_app
from app.orpheus import orpheus_blueprint
from app.zotify import zotify_blueprint
from app.utils import check_blueprint

# Crear y configurar la aplicación
app = create_app()

def setup_app(app):
    """
    Configura la aplicación Flask con los Blueprints.
    """
    app.register_blueprint(orpheus_blueprint)
    app.register_blueprint(zotify_blueprint)
    app.register_blueprint(check_blueprint)

    # Endpoint raíz para servir el frontend
    @app.route('/')
    def serve_frontend():
        return app.send_static_file('index.html')

# Configurar la aplicación
setup_app(app)

if __name__ == "__main__":
    # Leer host y puerto desde variables de entorno, con valores por defecto
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 7983))

    # Ejecutar el servidor en modo de desarrollo
    app.run(host=host, port=port)
