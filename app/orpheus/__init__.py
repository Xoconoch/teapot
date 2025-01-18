from flask import Blueprint

# Crear el blueprint de Orpheus
orpheus_blueprint = Blueprint('orpheus', __name__, url_prefix='/orpheus')

# Importar y registrar rutas en el Blueprint
from app.orpheus.download.album import album_download
from app.orpheus.download.track import track_download
from app.orpheus.search.album import search_album
from app.orpheus.search.track import search_track

orpheus_blueprint.add_url_rule('/download/album', view_func=album_download, methods=['GET'])
orpheus_blueprint.add_url_rule('/download/track', view_func=track_download, methods=['GET'])
orpheus_blueprint.add_url_rule('/search/album', view_func=search_album, methods=['POST'])
orpheus_blueprint.add_url_rule('/search/track', view_func=search_track, methods=['POST'])
