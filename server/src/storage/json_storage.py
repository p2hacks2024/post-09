import json
from typing import List

from models.activity import Activity

class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
    
    def read_activities(self) -> List[Activity]:
        data_dict = self.read()
        return [Activity(**activity) for activity in data_dict['activities']]

    def write_activities(self, activities: List[Activity]):
        data = {'activities': [activity.model_dump() for activity in activities]}
        self.write(data)