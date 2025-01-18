from flask import request, jsonify
from app.utils.docker import build_docker_command, run_docker_command
import re

def search_album():
    """
    Endpoint para buscar álbumes en Orpheus.
    """
    try:
        print("Inicio de search_album")

        data = request.get_json()
        print(f"Received data: {data}")

        required_fields = ["module", "query", "account"]
        for field in required_fields:
            if field not in data or not isinstance(data[field], str):
                error_message = f"Missing or invalid field: {field}. All fields must be strings."
                print(error_message)
                return jsonify({"error": error_message}), 400

        module = data["module"]
        query = data["query"]
        account = data["account"]

        print(f"Module: {module}, Account: {account}, Query: {query}")

        command = build_docker_command(account, module, "search", "album", query)
        print(f"Comando de Docker construido: {command}")

        try:
            result = run_docker_command(command)
            print(f"Raw Docker output: {result}")
        except Exception as e:
            error_message = f"Error executing search: {str(e)}"
            print(error_message)
            return jsonify({"error": "Error executing search", "output": str(e)}), 500

        output_lines = result.strip().split('\n')
        results = []

        for line in output_lines:
            line = line.strip()
            if line.lower().startswith("starting..."):
                continue

            match = re.match(r'^\d+\.\s(.+)\|(.+)\|(.+)\|(\d+)$', line)
            if match:
                album = match.group(1).strip()
                artist = match.group(2).strip()
                year = match.group(3).strip()
                album_id = match.group(4).strip()

                results.append({
                    "album": album,
                    "artist": artist,
                    "year": year,
                    "id": album_id
                })

        print(f"Resultados de búsqueda procesados: {results}")
        return jsonify({"message": "Search executed successfully", "results": results}), 200

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {str(e)}")
        return jsonify({"error": f"File error: {str(e)}"}), 404

    except KeyError as e:
        print(f"Error de clave: {str(e)}")
        return jsonify({"error": f"Key error: {str(e)}"}), 400

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
