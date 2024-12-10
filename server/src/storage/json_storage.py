import json
from typing import List

from models.activity import Activity
from storage.storage import Storage

class JsonStorage(Storage):
    '''
    JSONファイルを直接読み書きするためのクラス
    '''
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_file(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_file(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def create_user_activities(self, user_id: str, activities: List[Activity]):
        user_data_dict = {'user_id': user_id, 'activities': [activity.model_dump() for activity in activities]}
        data_dict = self._read_file()
        for user in data_dict['users']:
            if user['user_id'] == user_id:
                raise ValueError(f'User {user_id} already exists.')
        data_dict['users'].append(user_data_dict)
        self._write_file(data_dict)
        pass

    def read_user_activities(self, user_id: str) -> List[Activity]:
        data_dict = self._read_file()
        for user in data_dict['users']:
            if user['user_id'] == user_id:
                return [Activity(**activity) for activity in user['activities']]
        return [] #もしuser_idが存在しない場合は空リストを返す

    def update_user_activities(self, user_id: str, activities: List[Activity]):
        data_dict = self._read_file()
        if not data_dict['users']:
            # ユーザーデータが空の場合は新規作成
            self.create_user_activities(user_id, activities)
            return
        else:
            # ユーザーデータが存在する場合は更新
            for user in data_dict['users']:
                if user['user_id'] == user_id:
                    user['activities'] = [activity.model_dump() for activity in activities]
                    break
        self._write_file(data_dict)
    
    def delete_user_activities(self, user_id: str):
        data_dict = self._read_file()
        for user in data_dict['users']:
            if user['user_id'] == user_id:
                data_dict['users'].remove(user)
                break
        self._write_file(data_dict)
        pass
    
