import pytest

from analysis.analysis import Analysis
from models.activity import Activity, Music

@pytest.fixture
def analysis():
    return Analysis('tests/test_activities.json')

def test_get_activities(analysis):
    activities = analysis.get_activities()
    assert isinstance(activities, list) 

def test_add_activities(analysis):
    activities = analysis.get_activities()
    pre_len = len(activities)
    new_activity = Activity(timestamp='2021-01-01T00:00:00', 
                            emotion=[0.1, 0.2, 0.3],
                            weather='晴れ', 
                            temperature=20.0, 
                            music=Music(acousticness=0.5))
    analysis.add_activities(new_activity)
    
    activities = analysis.get_activities()
    assert len(activities) == pre_len + 1 # 1つ追加されているか確認
    assert activities[-1].timestamp == new_activity.timestamp
    assert activities[-1].emotion == new_activity.emotion
    assert activities[-1].weather == new_activity.weather
    assert activities[-1].temperature == new_activity.temperature
    assert activities[-1].music.acousticness == new_activity.music.acousticness