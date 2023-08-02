import json


def get_file_content(file_path):
    with open(file_path) as file:
        return file.read()


def parse_json(file_content):
    return json.loads(file_content)
