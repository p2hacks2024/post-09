import json

from models.activity import Activity

class JsonStrage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)