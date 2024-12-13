from pydantic import BaseModel
from typing import List
from datetime import datetime
from collections import defaultdict

from models.activity import Activity  # pyright: ignore

"""
exapmle:
@app.post("/analysis")
def analysis():
    storge = Storage("path")
    activities = storge.read_user_activities("0001")
    input = AnalysisInput(activities=activities)
    output = Analysis(input).output()
    return output.per_total
"""


class AnalysisInput(BaseModel):
    """
    分析用のリクエストボディ
    """

    activities: List[Activity]


class BaseOutput(BaseModel):
    """
    感情ごとの出現回数、感情ごとの出来事、出来事ごとの感情
    """

    emotion_freq: dict[str, int]
    emotion_to_situation: dict[str, List[str]]
    situation_to_emotion_freq: dict[str, dict[str, int]]


class AnalysisOutput(BaseModel):
    """
    分析結果のレスポンスボディ
    """

    per_total: BaseOutput
    per_year: BaseOutput
    per_month: BaseOutput
    per_week: BaseOutput
    per_day: BaseOutput


class Analysis:
    def __init__(self, input: AnalysisInput):
        self.activities = input.activities

    def output(self) -> AnalysisOutput:
        return AnalysisOutput(
            per_total=self._get_base_output("total"),
            per_year=self._get_base_output("year"),
            per_month=self._get_base_output("month"),
            per_week=self._get_base_output("weekday"),
            per_day=self._get_base_output("day"),
        )

    def _get_base_output(self, period: str) -> BaseOutput:
        """
        期間（period: total, year, month, weekday, day）ごとのBaseOutput
        """
        now_period = getattr(datetime.now(), period) if period != "total" else None

        emotion_freq: defaultdict[str, int] = defaultdict(int)
        emotion_to_situation: defaultdict[str, List[str]] = defaultdict(list)
        situation_to_emotion_freq: defaultdict[str, defaultdict[str, int]] = (
            defaultdict(lambda: defaultdict(int))
        )

        # 各要素の集計
        for activity in self.activities:
            activity_timestamp = datetime.strptime(
                activity.timestamp, "%Y-%m-%dT%H:%M:%S"
            )
            activity_period = (
                getattr(activity_timestamp, period) if period != "total" else None
            )
            if activity_period == now_period or period == "total":
                emotion_freq[activity.emotion] += 1
                emotion_to_situation[activity.emotion].append(activity.situation)
                situation_to_emotion_freq[activity.situation][activity.emotion] += 1

        return BaseOutput(
            emotion_freq=emotion_freq,
            emotion_to_situation=emotion_to_situation,
            situation_to_emotion_freq=dict(situation_to_emotion_freq),
        )
