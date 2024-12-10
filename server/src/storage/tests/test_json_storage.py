import pytest
from storage.json_storage import JsonStorage
from models.activity import Activity, Music

@pytest.fixture
def json_storage():
    return JsonStorage('test_data/test_activities.json')

def user_id():
    return '0003'

'''
test_create_and_read: user_id = '0003'のユーザーを追加
test_update: user_id = '0003'のユーザーを更新
test_delete: user_id = '0003'のユーザーを削除
'''

def test_create_and_read(json_storage):
    # アクティビティリストを追加
    activities_created = [Activity(timestamp='2021-01-01T00:00:00', 
                           emotion="anxiety", 
                           prompt="明日やだー",
                           situation="明日への不安", 
                           musics=[Music(acousticness=0.5)])]
    json_storage.create_user_activities(user_id(), activities_created)
    activities_read = json_storage.read_user_activities(user_id())
    assert activities_created[-1].emotion == activities_read[-1].emotion
    assert activities_created[-1].prompt == activities_read[-1].prompt
    assert activities_created[-1].situation == activities_read[-1].situation

def test_update(json_storage):
    # アクティビティリストを更新
    activities_updated = [Activity(timestamp='2021-01-01T00:00:00', 
                           emotion="sad", 
                           prompt="ぴえん",
                           situation="感情の落ち込み", 
                           musics=[Music(acousticness=0.5)])]
    json_storage.update_user_activities(user_id(), activities_updated)
    activities_read = json_storage.read_user_activities(user_id())
    assert activities_updated[0].emotion == activities_read[0].emotion
    assert activities_updated[0].prompt == activities_read[0].prompt
    assert activities_updated[0].situation == activities_read[0].situation

def test_delete(json_storage):
    # アクティビティリストを削除
    json_storage.delete_user_activities(user_id())
    activities_read = json_storage.read_user_activities(user_id())
    assert activities_read == []

