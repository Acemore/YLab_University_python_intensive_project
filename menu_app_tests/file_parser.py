import json
from typing import Any


def get_file_content(file_path) -> str:
    with open(file_path) as file:
        return file.read()


def parse_json(file_content) -> Any:
    return json.loads(file_content)
