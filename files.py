import os


def extract_filename_without_extension(path):
    """Extracts the filename without its extension from a given path"""
    base_name = os.path.basename(path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension


def read_txt_file(filepath):
    """Reads the content of a text file and returns it as a string"""
    with open(filepath, 'r') as file:
        content = file.read()

    return content
