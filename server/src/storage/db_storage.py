import sqlite3
from typing import List

from models.activity import Activity, Music  # pyright: ignore
from storage.storage import Storage  # pyright: ignore


class DBStorage(Storage):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY
        )
        """)

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TEXT,
                emotion TEXT,
                prompt TEXT,
                situation TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS musics (
            music_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER,
            name TEXT,
            genre TEXT,
            id TEXT,
            FOREIGN KEY (activity_id) REFERENCES activities (activity_id)
        )
        """)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # pyright: ignore
        self.conn.commit()
        self.conn.close()

    def _is_exist_user(self, user_id: str) -> bool:
        # user_idが存在するか確認
        self.c.execute(
            """
            SELECT user_id FROM users WHERE user_id = ?
        """,
            (user_id,),
        )
        return self.c.fetchone() is not None

    def _insert_user(self, user_id: str):
        # user_idをDBに追加
        self.c.execute(
            """
            INSERT INTO users (user_id) VALUES (?)
        """,
            (user_id,),
        )
        pass

    def _delete_user(self, user_id: str):
        # user_idをDBから削除
        self.c.execute(
            """
            DELETE FROM users WHERE user_id = ?
        """,
            (user_id,),
        )
        pass

    def _is_exist_activity(self, user_id: str) -> bool:
        # user_idに対してactivitiesが存在するか確認
        self.c.execute(
            """
            SELECT user_id FROM activities WHERE user_id = ?
        """,
            (user_id,),
        )
        return len(self.c.fetchall()) > 0

    def _get_existing_activities(self, user_id: str) -> List[Activity]:
        """
        指定されたuser_idに対応するactivitiesをDBから取得
        """
        self.c.execute(
            """
            SELECT * FROM activities WHERE user_id = ?
        """,
            (user_id,),
        )
        activities: List[Activity] = []
        for activity_row in self.c.fetchall():
            activity_id = activity_row[0]
            self.c.execute(
                """
                SELECT * FROM musics WHERE activity_id = ?
            """,
                (activity_id,),
            )
            musics: List[Music] = []
            for music_row in self.c.fetchall():
                musics.append(
                    Music(name=music_row[2], genre=music_row[3], id=music_row[4])
                )
            activity = Activity(
                timestamp=activity_row[2],
                emotion=activity_row[3],
                prompt=activity_row[4],
                situation=activity_row[5],
                musics=musics,
            )
            activities.append(activity)
        return activities

    def _insert_activities(self, user_id: str, activities: List[Activity]):
        """
        指定されたuser_idに対応するactivitiesをDBに新規追加
        """
        for activity in activities:
            self.c.execute(
                """
                INSERT INTO activities (
                    user_id, 
                    timestamp, 
                    emotion, 
                    prompt, 
                    situation) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    activity.timestamp,
                    activity.emotion,
                    activity.prompt,
                    activity.situation,
                ),
            )
            activity_id = self.c.lastrowid
            for music in activity.musics:
                self.c.execute(
                    """
                    INSERT INTO musics (activity_id, name, genre, id) VALUES (?, ?, ?, ?)
                """,
                    (activity_id, music.name, music.genre, music.id),
                )

    def _update_activities(self, user_id: str, new_activities: List[Activity]):
        """
        指定されたuser_idに対応するactivitiesをDBに更新
        """
        existing_activities = self._get_existing_activities(user_id)

        for new_activity in new_activities:
            # 既存のアクティビティを検索
            existing_activity = None
            for activity in existing_activities:
                if activity.timestamp == new_activity.timestamp:
                    existing_activity = activity
                    break

            if existing_activity is not None:
                # 差分がある場合のみ更新
                if (
                    existing_activity.emotion != new_activity.emotion
                    or existing_activity.prompt != new_activity.prompt
                    or existing_activity.situation != new_activity.situation
                ):
                    self.c.execute(
                        """
                        UPDATE activities 
                        SET emotion = ?, prompt = ?, situation = ?
                        WHERE user_id = ? AND timestamp = ? 
                    """,
                        (
                            new_activity.emotion,
                            new_activity.prompt,
                            new_activity.situation,
                            user_id,
                            new_activity.timestamp,
                        ),
                    )

                # 音楽情報の更新
                for new_music in new_activity.musics:
                    self.c.execute(
                        """
                        UPDATE musics
                        SET name = ?
                        SET genre = ?
                        SET id = ?
                        WHERE activity_id = (
                            SELECT activity_id FROM activities WHERE user_id = ? AND timestamp = ?
                        )
                    """,
                        (
                            new_music.name,
                            new_music.genre,
                            new_music.id,
                            user_id,
                            new_activity.timestamp,
                        ),
                    )
            else:
                # 新しいアクティビティを挿入
                self.c.execute(
                    """
                    INSERT INTO activities (user_id, timestamp, emotion, prompt, situation) VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        new_activity.timestamp,
                        new_activity.emotion,
                        new_activity.prompt,
                        new_activity.situation,
                    ),
                )
                activity_id = self.c.lastrowid
                for new_music in new_activity.musics:
                    self.c.execute(
                        """
                        INSERT INTO musics (activity_id, name, genre, id) VALUES (?, ?, ?, ?)
                    """,
                        (activity_id, new_music.name, new_music.genre, new_music.id),
                    )

    def _delete_activities(self, user_id: str):
        """
        指定されたuser_idに対応するactivitiesをDBから削除
        """
        self.c.execute(
            """
            DELETE FROM activities WHERE user_id = ?
        """,
            (user_id,),
        )
        self.c.execute("""
            DELETE FROM musics WHERE activity_id NOT IN (SELECT activity_id FROM activities)
        """)

    def create_user_activities(self, user_id: str, activities: List[Activity]):
        """
        Create: activitiesをDBに新規追加
        user_idが存在しない場合 -> user_idをDBに新規追加, activitiesをDBに新規追加
        user_idが存在するがactivitiesが存在しない場合 -> activitiesをDBに新規追加
        user_idが存在しactivitiesも存在する場合 -> 既に存在するためエラーを返す
        """
        if not self._is_exist_user(user_id):
            # user_idが存在しない場合
            print("user_id:", user_id, "is not exist.")
            self._insert_user(user_id)  # user_idをDBに新規追加
            self._insert_activities(user_id, activities)  # activitiesをDBに新規追加
        elif not self._is_exist_activity(user_id):
            # user_idが存在するがactivitiesが存在しない場合
            print("user_id:", user_id, "is exist but activities is not exist.")
            self._insert_activities(user_id, activities)  # activitiesをDBに新規追加
        else:
            # user_idが存在しactivitiesも存在する場合
            raise ValueError(
                f"User {user_id}s activities already exists."
            )  # 既に存在するためエラーを返す
        self.conn.commit()

    def read_user_activities(self, user_id: str) -> List[Activity]:
        """
        Read: activitiesをDBから取得
        user_idが存在しない場合 -> 空のリストを返す
        user_idが存在するがactivitiesが存在しない場合 -> 空のリストを返す
        """
        # user_idが既に存在するか確認
        if not self._is_exist_user(user_id) or not self._is_exist_activity(user_id):
            print("user_id:", user_id, "is not exist.")
            return []
        else:
            return self._get_existing_activities(user_id)

    def update_user_activities(self, user_id: str, activities: List[Activity]):
        """
        Update: activitiesをDBに更新
        user_idが存在しない場合 -> エラーを返す
        user_idが存在するがactivitiesが存在しない場合 -> エラーを返す
        user_idが存在しactivitiesも存在する場合 -> activitiesをDBに更新
        """
        if not self._is_exist_user(user_id):
            raise ValueError(f"User {user_id} does NOT exist.")
        elif not self._is_exist_activity(user_id):
            raise ValueError(f"User {user_id} does NOT have any activities.")

        self._update_activities(user_id, activities)
        self.conn.commit()

    def delete_user_activities(self, user_id: str):
        """
        Delete: activitiesをDBから削除
        user_idが存在しない場合 -> 何もしない
        user_idが存在するがactivitiesが存在しない場合 -> エラーを返す
        user_idが存在しactivitiesも存在する場合 -> activitiesをDBから削除
        """
        if not self._is_exist_user(user_id):
            # user_idが存在しない場合 -> 何もしない
            return
        if not self._is_exist_activity(user_id):
            # user_idが存在するがactivitiesが存在しない場合 -> 削除するものがない
            raise ValueError(f"User {user_id} does NOT have any activities.")
        else:
            # user_idが存在しactivitiesも存在する場合 -> 削除するものがある
            print("user_id:", user_id, "is exist and activities is exist.")
            self._delete_activities(user_id)
        self.conn.commit()
