import pytest

from analysis.analysis import Analysis
from models.activity import Activity, Music

@pytest.fixture
def analysis():
    return Analysis('test_data/test_activities.json')
