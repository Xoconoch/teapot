from flask import request, jsonify
from app.utils.docker import build_docker_command, run_docker_command
import re

def search_track():
    """
    Endpoint para buscar pistas en Orpheus.
    """
    try:
        # Registrar inicio de la solicitud
        print("Inicio de search_track")

        # Obtener los parámetros de la solicitud
        data = request.get_json()

        # Verificar campos requeridos
        required_fields = ["module", "query"]
        for field in required_fields:
            if field not in data or not isinstance(data[field], str):
                print(f"Falta o campo inválido: {field}")
                return jsonify({"error": f"Missing or invalid field: {field}. All fields must be strings."}), 400

        module = data["module"]
        query = data["query"]
        account = data.get("account")  # Campo opcional

        # Construir el comando  (docker.py handles module replacement now)
        command = build_docker_command(account, module, "search", "track", query)
        print(f"Comando de Docker construido: {command}")

        try:
            result = run_docker_command(command)
            print(f"Raw Docker output: {result}")
        except Exception as e:
            error_message = f"Error executing search: {str(e)}"
            print(error_message)
            return jsonify({"error": "Error executing search", "output": str(e)}), 500


        # Procesar la salida
        output_lines = result.strip().split('\n')
        tracks = []

        for line in output_lines:
            line = line.strip()
            if line.lower().startswith("starting..."):
                continue

            match = re.match(r'^\d+\.\s(.+)\|(.+)\|(.+)\|(\d+)$', line)
            if match:
                title = match.group(1).strip()
                artist = match.group(2).strip()
                year = match.group(3).strip()
                track_id = match.group(4).strip()

                tracks.append({
                    "title": title,
                    "artist": artist,
                    "year": year,
                    "id": track_id
                })

        print(f"Resultados de búsqueda procesados: {tracks}")
        return jsonify({"message": "Search executed successfully", "results": tracks}), 200


    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {str(e)}")
        return jsonify({"error": f"File error: {str(e)}"}), 404

    except KeyError as e:
        print(f"Error de clave: {str(e)}")
        return jsonify({"error": f"Key error: {str(e)}"}), 400

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
