import pytest
from storage.json_storage import JsonStorage
from models.activity import Activity

@pytest.fixture
def json_storage():
    return JsonStorage('test_data/test_activities.json')

def test_read(json_storage):
    data = json_storage.read()
    assert isinstance(data, dict)
    assert 'activities' in data

def test_load_activities(json_storage):
    activities = json_storage.load_activities()
    print(activities)
    assert isinstance(activities, list)

def test_save_activities(json_storage):
    activities = [Activity(timestamp='2021-01-01T00:00:00', 
                           emotion=[0.1, 0.2, 0.3, 0.4], weather='晴れ',
                           temperature=20.0, 
                           music={'acousticness': 0.5})]
    json_storage.save_activities(activities)
    activities = json_storage.load_activities()
    assert len(activities) == 1
    assert activities[0].timestamp == '2021-01-01T00:00:00'
    assert activities[0].emotion == [0.1, 0.2, 0.3, 0.4]
    assert activities[0].weather == '晴れ'
    assert activities[0].temperature == 20.0
    assert activities[0].music.acousticness == 0.5