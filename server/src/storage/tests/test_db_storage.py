import pytest
from storage.db_storage import DBStorage  # pyright: ignore
from models.activity import Activity, Music  # pyright: ignore


@pytest.fixture
def db_storage() -> DBStorage:
    return DBStorage("./db/test_activities.db")


def user_id() -> str:
    return "0002"


def test_instance(db_storage: DBStorage) -> None:
    assert isinstance(db_storage, DBStorage)


def test_create_and_read_user_activities(db_storage: DBStorage) -> None:
    activitites_created = [
        Activity(
            timestamp="2021-01-01T00:00:01",
            emotion="孤独感",
            prompt="楽しい",
            situation="友達と遊ぶ",
            musics=[
                Music(track_name="hi", track_id="01", album_id="01", popularity=1),
            ],
        ),
        Activity(
            timestamp="2021-01-02T00:00:01",
            emotion="不安",
            prompt="うーん",
            situation="日曜日",
            musics=[
                Music(track_name="bye", track_id="02", album_id="02", popularity=2),
            ],
        ),
    ]
    db_storage.create_user_activities(user_id(), activitites_created)
    activities_read = db_storage.read_user_activities(user_id())
    print(activities_read)
    assert activitites_created[0].emotion == activities_read[0].emotion
    assert activitites_created[0].prompt == activities_read[0].prompt
    assert activitites_created[0].situation == activities_read[0].situation


def test_update_user_activities(db_storage: DBStorage) -> None:
    activitites_updated = [
        Activity(
            timestamp="2021-01-02T01:00:00",
            emotion="悲しみ",
            prompt="ぴえん",
            situation="感情の落ち込み",
            musics=[
                Music(track_name="cry", track_id="03", album_id="03", popularity=3)
            ],
        )
    ]
    db_storage.update_user_activities(user_id(), activitites_updated)
    activities_read = db_storage.read_user_activities(user_id())
    print(activities_read)
    assert activitites_updated[-1].emotion == activities_read[-1].emotion
    assert activitites_updated[-1].prompt == activities_read[-1].prompt
    assert activitites_updated[-1].situation == activities_read[-1].situation


def test_delete_user_activities(db_storage: DBStorage) -> None:
    db_storage.delete_user_activities(user_id())
    activities_read = db_storage.read_user_activities(user_id())
    assert activities_read == []
