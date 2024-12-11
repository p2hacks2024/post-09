import pytest

from storage.json_storage import JsonStorage
from analysis.analysis import Analysis, AnalysisInput, AnalysisOutput, BaseOutput
from models.activity import Activity, Music

@pytest.fixture
def analysis():
    storage = JsonStorage('test_data/test_activities.json')
    activities = storage.read_user_activities('0001')
    input = AnalysisInput(activities=activities)
    return Analysis(input)


def test_get_base_output(analysis):
    out = analysis._get_base_output('month')
    assert out.emotion_freq == {'sad': 2}
    assert out.emotion_to_situation == {'sad': ['忘れ物', '悪夢を見た']}
    assert out.situation_to_emotion_freq == {'忘れ物': {'sad': 1}, '悪夢を見た': {'sad': 1}}

def test_output(analysis):
    output = analysis.output()
    assert output.per_total.emotion_freq == {'sad': 2}
    assert output.per_total.emotion_to_situation == {'sad': ['忘れ物', '悪夢を見た']}
    assert output.per_total.situation_to_emotion_freq == {'忘れ物': {'sad': 1}, '悪夢を見た': {'sad': 1}}