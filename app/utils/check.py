import os
from flask import Blueprint, jsonify

check_blueprint = Blueprint('check', __name__)

def scan_directory(directory):
    results = {}

    if not directory or not os.path.isdir(directory):
        return results

    # Primer recorrido: Listar subdirectorios de nivel 1
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)

        if os.path.isdir(subdir_path):
            # Agregar subdirectorio al resultado (sin sub-subdirectorios)
            results[subdir] = []

            # Listar subdirectorios dentro del subdirectorio (1 nivel)
            for item in os.listdir(subdir_path):
                if os.path.isdir(os.path.join(subdir_path, item)):
                    results[subdir].append(item)

    return results

@check_blueprint.route('/check', methods=['GET'])
def check_creds_directory():
    creds_dir = '/app/credentials'

    if not creds_dir:
        return jsonify({"error": "Creds dir not set"}), 400

    scan_results = scan_directory(creds_dir)
    return jsonify(scan_results)
