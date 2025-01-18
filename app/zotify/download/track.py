import re
import subprocess
import os
from flask import Blueprint, request, jsonify, Response

zotify_download_track_bp = Blueprint('zotify_download_track', __name__)

@zotify_download_track_bp.route('/download/track', methods=['GET'])
def zotify_download_track():
    """
    Endpoint para descargar un track usando Zotify.
    """
    try:
        # Obtener los parámetros del query string
        track_url = request.args.get('url')
        account = request.args.get('account')

        # Validación de los parámetros requeridos
        if not track_url:
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
            track_url
        ]

        def stream_output():
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            track_info_sent = False

            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if not line:
                    continue

                # Extraer información del track y el artista
                if not track_info_sent:
                    match = re.search(r'Descargando track \"(.+?)\" de \"(.+?)\"', line)
                    if match:
                        track_name = match.group(1)
                        artist_name = match.group(2)
                        yield f"data: {{\"track\": \"{track_name}\"}}\n\n"
                        yield f"data: {{\"artist\": \"{artist_name}\"}}\n\n"
                        track_info_sent = True

            process.stdout.close()
            process.wait()

            # Emitir un mensaje final basado en el resultado del comando
            if process.returncode == 0:
                yield "data: {\"message\": \"Download complete\"}\n\n"
            else:
                error_message = process.stderr.read().strip()
                yield f"data: {{\"error\": \"{error_message}\"}}\n\n"

        return Response(stream_output(), content_type="text/event-stream")

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
