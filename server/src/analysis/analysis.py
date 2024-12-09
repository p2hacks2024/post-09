
from typing import List

from models.activity import Activity
from storage.json_storage import JsonStorage

class Analysis:
    def __init__(self, storage_path: str):
        '''
        storage_path: str - アクティビティの保存先
        storage: JsonStorage - JsonStorageのインスタンス
        activities: List[Activity] - アクティビティのリスト
        '''
        self.storage_path = storage_path
        self.storage = JsonStorage(self.storage_path)
        self.activities = self.storage.load_activities()

    def get_activities(self) -> List[Activity]:
        return self.activities
    
    def add_activities(self, new_activity: Activity):
        self.activities.append(new_activity)
        self.storage.save_activities(self.activities)