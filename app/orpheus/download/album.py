from flask import request, jsonify, Response
from app.utils.docker import build_docker_command
from app.utils.album_utils import parse_album_output
from app.utils.track_utils import parse_track_output
import subprocess
import json

def album_download():
    """
    Endpoint para descargar un álbum de Orpheus.
    """
    try:
        # Registrar inicio de la solicitud
        print("Inicio de album_download")

        # Obtener los parámetros de la solicitud
        module = request.args.get('module')
        album_id = request.args.get('id')
        account = request.args.get('account')

        # Validar que los parámetros requeridos están presentes
        if not all([module, album_id, account]):
            print("Faltan parámetros: account, module, y id son requeridos.")
            return jsonify({"error": "Missing required parameters: module, id and account are required."}), 400

        # Construir el comando de Docker
        command = build_docker_command(account, module, "download", "album", album_id)
        print(f"Comando de Docker construido: {command}")

        def stream_output():
            print("Iniciando proceso de Docker")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            parser = None

            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    print(f"Salida de Docker: {line}")

                    if parser is None:
                        response = parse_album_output(line)
                        if response is not None:
                            parser = parse_album_output
                        else:
                            response = parse_track_output(line)
                            if response is not None:
                                parser = parse_track_output

                    else:
                        response = parser(line)

                    if response is not None:
                        yield f"data: {json.dumps(response)}\n\n"

            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                error_message = process.stderr.read().strip()
                print(f"Error en Docker: {error_message}")
                yield f"data: {json.dumps({'error': error_message})}\n\n"

        return Response(stream_output(), content_type="text/event-stream")

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {str(e)}")
        return jsonify({"error": f"File error: {str(e)}"}), 404

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
