from flask import request, jsonify, Response
from app.utils.docker import build_docker_command
from app.utils.track_utils import parse_track_output
import subprocess
import json

def track_download():
    """
    Endpoint para descargar una pista de Orpheus.
    """
    try:
        # Registrar inicio de la solicitud
        print("Inicio de track_download")

        # Obtener parámetros de la solicitud
        module = request.args.get('module')
        track_id = request.args.get('id')
        account = request.args.get('account')  # Campo opcional

        # Validar parámetros requeridos
        if not all([module, track_id, account]):
            print("Faltan parámetros: account, module y id son requeridos.")
            return jsonify({"error": "Missing required parameters: module, id and account are required."}), 400

        # Construir el comando de Docker  (Corrected line)
        command = build_docker_command(account, module, "download", "track", track_id)
        print(f"Comando de Docker construido: {command}")

        def stream_output():
            print("Iniciando proceso de Docker")
            # Ejecutar el proceso de Docker
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    # Usar parse_track_output para procesar la salida
                    print(f"Salida de Docker: {line}")
                    response = parse_track_output(line)
                    if response is not None:
                        yield f"data: {json.dumps(response)}\n\n"

            process.stdout.close()
            process.wait()

            # Manejar errores del proceso
            if process.returncode != 0:
                error_message = process.stderr.read().strip()
                print(f"Error en Docker: {error_message}")
                yield f"data: {json.dumps({'error': error_message})}\n\n"

        return Response(stream_output(), content_type="text/event-stream")

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {str(e)}")
        return jsonify({"error": f"File error: {str(e)}"}), 404

    except Exception as e: # Simplified exception handling
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
