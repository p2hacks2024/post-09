import pytest
from storage.json_storage import JsonStorage
from models.activity import Activity, Music

@pytest.fixture
def json_storage():
    return JsonStorage('test_data/test_activities.json')

'''
test_create_and_read: user_id = '0002'のユーザーを追加
test_update: user_id = '0002'のユーザーを更新
test_delete: user_id = '0002'のユーザーを削除
'''

def test_create_and_read(json_storage):
    # アクティビティリストを追加
    user_id = '0002'
    activities_created = [Activity(timestamp='2021-01-01T00:00:00', 
                           emotion="sad", 
                           prompt="What's wrong?",
                           situation="work", 
                           musics=[Music(acousticness=0.5)])]
    json_storage.create_user_activities(user_id, activities_created)
    activities_read = json_storage.read_user_activities(user_id)
    assert activities_created == activities_read

def test_update(json_storage):
    # アクティビティリストを更新
    user_id = '0002'
    activities_updated = [Activity(timestamp='2021-01-01T00:00:00', 
                           emotion="sad", 
                           prompt="What's wrong?",
                           situation="work", 
                           musics=[Music(acousticness=0.5)])]
    json_storage.update_user_activities(user_id, activities_updated)
    activities_read = json_storage.read_user_activities(user_id)
    assert activities_updated == activities_read

def test_delete(json_storage):
    # アクティビティリストを削除
    user_id = '0002'
    json_storage.delete_user_activities(user_id)
    activities_read = json_storage.read_user_activities(user_id)
    assert activities_read == []

