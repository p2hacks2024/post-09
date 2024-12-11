from calendar import c
import sqlite3
from typing import List

from models.activity import Activity, Music
from storage.storage import Storage

class DBStorage(Storage):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY
        )
        ''')

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TEXT,
                emotion TEXT,
                prompt TEXT,
                situation TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS musics (
            music_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER,
            acousticness REAL,
            FOREIGN KEY (activity_id) REFERENCES activities (activity_id)
        )
        ''')
        self.conn.commit()
    
    def _get_user_db_id(self, user_id: str) -> int:
        self.c.execute('''
            SELECT ROW_NUMBER() OVER (ORDER BY user_id) AS row_num, user_id FROM users WHERE user_id = ?
        ''', (user_id,))
        return self.c.fetchone()[0]
    
    def _is_exit_user(self, user_id: str) -> bool:
        # user_idが存在するか確認
        self.c.execute('''
            SELECT user_id FROM users WHERE user_id = ?
        ''', (user_id,))
        return self.c.fetchone() is not None
    
    def _insert_user(self, user_id: str):
        # user_idをDBに追加
        self.c.execute('''
            INSERT INTO users (user_id) VALUES (?)
        ''', (user_id,))
        pass

    def _delete_user(self, user_id: str):
        # user_idをDBから削除
        self.c.execute('''
            DELETE FROM users WHERE user_id = ?
        ''', (user_id,))
        pass
    
    def _is_exit_activity(self, user_id: str) -> bool:
        # user_idに対してactivitiesが存在するか確認
        self.c.execute('''
            SELECT user_id FROM activities WHERE user_id = ?
        ''', (self._get_user_db_id(user_id),))
        return len(self.c.fetchall()) > 0
    
    def _insert_activities(self, user_id: str, activities: List[Activity]):
        '''
        指定されたuser_idに対応するactivitiesをDBに新規追加
        '''
        user_db_id = self._get_user_db_id(user_id)
        for activity in activities:
            self.c.execute('''
                INSERT INTO activities (user_id, timestamp, emotion, prompt, situation) VALUES (?, ?, ?, ?, ?)
            ''', (user_db_id, 
                  activity.timestamp, 
                  activity.emotion, 
                  activity.prompt, 
                  activity.situation))
            activity_db_id = self.c.lastrowid
            for music in activity.musics:
                self.c.execute('''
                    INSERT INTO musics (activity_id, acousticness) VALUES (?, ?)
                ''', (activity_db_id, music.acousticness))
        pass

    def _delete_activities(self, user_id: str):
        '''
        指定されたuser_idに対応するactivitiesをDBから削除
        '''
        user_db_id = self._get_user_db_id(user_id)
        self.c.execute('''
            DELETE FROM activities WHERE user_id = ?
        ''', (user_db_id,))
        self.c.execute('''
            DELETE FROM musics WHERE activity_id NOT IN (SELECT activity_id FROM activities)
        ''')
        pass
    
    def create_user_activities(self, user_id: str, activities: List[Activity]):
        '''
        Create: activitiesをDBに新規追加
        user_idが存在しない場合 -> user_idをDBに新規追加
        user_idが存在するがactivitiesが存在しない場合 -> activitiesをDBに新規追加
        user_idが存在しactivitiesも存在する場合 -> 既に存在するためエラーを返す
        '''
        if not self._is_exit_user(user_id):
            # user_idが存在しない場合
            print("user_id:",user_id, "is not exist.")
            self._insert_user(user_id) # user_idをDBに新規追加
            self._insert_activities(user_id, activities) # activitiesをDBに新規追加
        elif not self._is_exit_activity(user_id):
            # user_idが存在するがactivitiesが存在しない場合
            print("user_id:",user_id, "is exist but activities is not exist.")
            self._insert_activities(user_id, activities) # activitiesをDBに新規追加
        else:
            # user_idが存在しactivitiesも存在する場合
            raise ValueError(f'User {user_id}s activities already exists.') # 既に存在するためエラーを返す
        self.conn.commit()

    def read_user_activities(self, user_id: str) -> List[Activity]:
        '''
        Read: activitiesをDBから取得
        user_idが存在しない場合 -> 空のリストを返す
        user_idが存在するがactivitiesが存在しない場合 -> 空のリストを返す
        '''
        # user_idが既に存在するか確認
        if not self._is_exit_user(user_id) or not self._is_exit_activity(user_id):
            print("user_id:",user_id, "is not exist.")
            return []
        
        self.c.execute('''
            SELECT * FROM activities WHERE user_id = ?
        ''', (self._get_user_db_id(user_id),))
        activities = []
        rows = self.c.fetchall()
        print(rows)
        for activity_row in rows :
            activity_db_id = self.c.lastrowid
            self.c.execute('''
                SELECT acousticness FROM musics WHERE activity_id = ?
            ''', (activity_db_id,))
            musics = []
            for music_row in self.c.fetchall():
                musics.append(Music(acousticness=music_row[0]))
            activity = Activity(
                timestamp=activity_row[2],
                emotion=activity_row[3],
                prompt=activity_row[4],
                situation=activity_row[5],
                musics=musics
            )
            activities.append(activity)
        return activities

    def update_user_activities(self, user_id: str, activities: List[Activity]):
        '''
        Update: activitiesをDBに更新
        user_idが存在しない場合 -> エラーを返す
        user_idが存在するがactivitiesが存在しない場合 -> エラーを返す
        user_idが存在しactivitiesも存在する場合 -> activitiesをDBに更新
        '''
        if not self._is_exit_user(user_id):
            raise ValueError(f'User {user_id} does NOT exist.')
        elif not self._is_exit_activity(user_id):
            raise ValueError(f'User {user_id} does NOT have any activities.')

        self._delete_activities(user_id)
        self._insert_activities(user_id, activities)
        self.conn.commit()
        pass
    
    def delete_user_activities(self, user_id: str):
        '''
        Delete: activitiesをDBから削除
        user_idが存在しない場合 -> エラーを返す
        user_idが存在するがactivitiesが存在しない場合 -> エラーを返す
        user_idが存在しactivitiesも存在する場合 -> activitiesをDBから削除
        '''
        if not self._is_exit_user(user_id):
            # user_idが存在しない場合 -> 削除するものがない
            raise ValueError(f'User {user_id} does NOT exist.')
        elif not self._is_exit_activity(user_id):
            # user_idが存在するがactivitiesが存在しない場合 -> 削除するものがない
            raise ValueError(f'User {user_id} does NOT have any activities.')
        else:
            # user_idが存在しactivitiesも存在する場合 -> 削除するものがある
            print("user_id:",user_id, "is exist and activities is exist.")
            self._delete_activities(user_id)
        self.conn.commit()

        pass