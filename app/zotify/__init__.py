from flask import Blueprint

# Crear el blueprint de Zotify
zotify_blueprint = Blueprint('zotify', __name__, url_prefix='/zotify')

# Importar y registrar rutas
from app.zotify.download.album import zotify_download_album
from app.zotify.download.track import zotify_download_track  # Importa el nuevo endpoint

zotify_blueprint.add_url_rule('/download/album', view_func=zotify_download_album, methods=['GET'])
zotify_blueprint.add_url_rule('/download/track', view_func=zotify_download_track, methods=['GET'])  # Registra el nuevo endpoint
