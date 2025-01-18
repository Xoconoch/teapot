import os
import json

def replace_modules(module_name: str, module_file_name: str) -> dict:
    """
    Reemplaza únicamente la subclave correspondiente al módulo especificado dentro de `modules` en `settings.json`.

    Args:
        module_name (str): Nombre del módulo.
        module_file_name (str): Nombre del archivo del módulo.

    Returns:
        dict: Contenido actualizado del archivo `settings.json`.

    Raises:
        EnvironmentError: Si las variables de entorno necesarias no están configuradas.
        FileNotFoundError: Si los archivos necesarios no existen.
        KeyError: Si el archivo del módulo no contiene la clave 'modules'.
    """
    # Obtener rutas
    orpheus_conf_dir = ("/app/config")
    creds_dir = ("/app/credentials")

    if not orpheus_conf_dir or not creds_dir:
        raise EnvironmentError("Las variables de entorno ORPHEUS_CONF_DIR y CREDS_DIR deben estar configuradas.")

    # Rutas de archivos
    settings_file_path = os.path.join(orpheus_conf_dir, "settings.json")
    module_file_path = os.path.join(creds_dir, module_name, module_file_name)

    # Verificar existencia de archivos
    if not os.path.isfile(settings_file_path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {settings_file_path}")

    if not os.path.isfile(module_file_path):
        raise FileNotFoundError(f"No se encontró el archivo del módulo: {module_file_path}")

    # Leer y cargar datos de JSON
    with open(settings_file_path, "r") as settings_file:
        settings_data = json.load(settings_file)

    with open(module_file_path, "r") as module_file:
        module_data = json.load(module_file)

    # Reemplazar únicamente la subclave del módulo específico
    if "modules" not in module_data or module_name not in module_data["modules"]:
        raise KeyError(f"El archivo del módulo no contiene la clave 'modules' o el módulo '{module_name}'.")

    # Actualizar subclave del módulo
    settings_data.setdefault("modules", {})[module_name] = module_data["modules"][module_name]

    # Guardar el archivo actualizado
    with open(settings_file_path, "w") as settings_file:
        json.dump(settings_data, settings_file, indent=4)

    return settings_data
