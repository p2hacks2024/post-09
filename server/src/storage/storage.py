from abc import ABC, abstractmethod
from typing import List

from models.activity import Activity

class Storage(ABC):
    '''
    CRUD操作を提供する抽象クラス
    '''
    @abstractmethod
    def create_user_activities(self, user_id: str, activities: List[Activity]):
        pass

    @abstractmethod
    def read_user_activities(self, user_id: str) -> List[Activity]:
        pass

    @abstractmethod
    def update_user_activities(self, user_id: str, activities: List[Activity]):
        pass

    @abstractmethod
    def delete_user_activities(self, user_id: str):
        pass