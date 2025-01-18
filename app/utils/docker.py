import subprocess
import os

def build_docker_command(account, module, *args):
    """Construye el comando para ejecutar el contenedor Docker (Orpheus)."""
    credentials_dir = "/app/credentials"
    dl_dir = os.environ.get("ORPHEUS_DL_DIR", "/app/downloads")

    print(f"DEBUG: Building Docker command for module: {module}, account: {account}")

    command = [
        "docker", "run", "--rm", "-t",
        "-v", f"{credentials_dir}/{module}/{account}:/app/config",
        "-v", f"{dl_dir}:/app/downloads",
        "orpheusdl", "python3", "orpheus.py"
    ]

    if args: # Check if args is not empty
        command.extend(args[:1]) # Add the first argument (e.g., 'download')
        command.append(module)    # Add the module after the first argument
        command.extend(args[1:]) # Add the remaining arguments

    else: # Handle the case where *args is empty
        command.append(module)


    print(f"DEBUG: Full Docker command: {command}")
    return command

def run_docker_command(command):
    """Ejecuta un comando Docker y retorna el resultado."""
    print(f"DEBUG: Running Docker command: {command}")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"DEBUG: Docker command failed with stderr:\n{result.stderr}")
        raise Exception(f"Error: {result.stderr}")
    else:
        print(f"DEBUG: Docker command stdout:\n{result.stdout}")
        return result.stdout
