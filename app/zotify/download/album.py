import re
import subprocess
import os
from flask import Blueprint, request, jsonify, Response

zotify_download_album_bp = Blueprint('zotify_download_album', __name__)

@zotify_download_album_bp.route('/download/album', methods=['GET'])
def zotify_download_album():
    """
    Endpoint para descargar un álbum usando Zotify.
    """
    try:
        # Obtener los parámetros del query string
        album_url = request.args.get('url')
        account = request.args.get('account')

        # Validación de los parámetros requeridos
        if not album_url:
            return jsonify({"error": "Missing required parameter: url is required."}), 400

        if not account or not re.match(r'^\S+$', account):
            return jsonify({"error": "Missing or invalid parameter: account must be a non-empty string without spaces."}), 400

        # Obtener las variables de entorno y definir rutas
        creds_dir = '/app/credentials'
        orpheus_dl_dir = '/app/downloads'

        # Construcción del directorio de credenciales basado en la variable de entorno
        credentials_path = f"{creds_dir}/spotify/{account}"

        # Construcción del comando a ejecutar
        command = [
            "docker", "run", "--rm",
            "-v", f"{orpheus_dl_dir}:/root/Music/Zotify Music",
            "-v", f"{credentials_path}:/app/zotify/credentials",
            "zotify",
            "python3", "-m", "zotify",
            "--credentials-location", "/app/zotify/credentials/credentials.json",
            "--download-lyrics", "false",
            album_url
        ]

        def stream_output():
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            album_info_sent = False

            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if not line:
                    continue

                if not album_info_sent:
                    match = re.search(r"Descargando el álbum '(.+?)' de (.+?) con (\d+) pistas", line)
                    if match:
                        album_name = match.group(1)
                        artist_name = match.group(2)
                        total_tracks = int(match.group(3))
                        yield f"data: {{\"album\": \"{album_name}\", \"artist\": \"{artist_name}\", \"total\": {total_tracks}}}\n\n"
                        album_info_sent = True
                        continue

                match_download = re.search(r"Descarga exitosa: (\d+)/(\d+)", line)
                if match_download:
                    downloaded_tracks = int(match_download.group(1))
                    yield f"data: {{\"downloaded\": {downloaded_tracks}, \"total\": {total_tracks}}}\n\n"


            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                yield "data: {\"message\": \"Download complete\"}\n\n"
            else:
                error_message = process.stderr.read().strip()
                yield f"data: {{\"error\": \"{error_message}\"}}\n\n"

        return Response(stream_output(), content_type="text/event-stream")

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
