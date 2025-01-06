import zipfile
import os


UNITS = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']


def get_file_size(path):

    if os.path.isdir(path):
        return "-"

    bytes_size = os.path.getsize(path)

    index = 0
    while bytes_size >= 1024 and index < len(UNITS) - 1:
        bytes_size /= 1024
        index += 1

    return f"{bytes_size:.2f} {UNITS[index]}"


def get_folder_size(folder_path):
    """Calcula el tamaño total de una carpeta y la devuelve en la unidad más cercana."""
    if not os.path.isdir(folder_path):
        return "El path no es una carpeta"

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.exists(file_path):  # Verificar que el archivo exista
                total_size += os.path.getsize(file_path)

    # Calcular la unidad más cercana
    index = 0
    while total_size >= 1024 and index < len(UNITS) - 1:
        total_size /= 1024
        index += 1

    return f"{total_size:.2f} {UNITS[index]}"


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, relative_path)