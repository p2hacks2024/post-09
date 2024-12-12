import pytest
from storage.db_storage import DBStorage  # pyright: ignore
from models.activity import Activity, Music  # pyright: ignore


@pytest.fixture
def db_storage() -> DBStorage:
    return DBStorage("./db/test_activitites.db")


def user_id() -> str:
    return "0001"


def test_instance(db_storage: DBStorage) -> None:
    assert isinstance(db_storage, DBStorage)


def test_create_and_read_user_activities(db_storage: DBStorage) -> None:
    activitites_created = [
        Activity(
            timestamp="2021-01-01T00:00:00",
            emotion="happy",
            prompt="楽しい",
            situation="友達と遊ぶ",
            musics=[
                Music(name="hi", genre="jazz", id="01"),
            ],
        ),
        Activity(
            timestamp="2021-01-02T00:00:00",
            emotion="anxiety",
            prompt="うーん",
            situation="日曜日",
            musics=[
                Music(name="hi", genre="jazz", id="01"),
            ],
        ),
    ]
    db_storage.create_user_activities(user_id(), activitites_created)
    activities_read = db_storage.read_user_activities(user_id())
    print(activities_read)
    assert activitites_created[-1].emotion == activities_read[-1].emotion
    assert activitites_created[-1].prompt == activities_read[-1].prompt
    assert activitites_created[-1].situation == activities_read[-1].situation


def test_update_user_activities(db_storage: DBStorage) -> None:
    activitites_updated = [
        Activity(
            timestamp="2021-01-02T01:00:00",
            emotion="sad",
            prompt="ぴえん",
            situation="感情の落ち込み",
            musics=[Music(name="hi", genre="jazz", id="01")],
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
