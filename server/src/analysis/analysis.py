from pydantic import BaseModel
from typing import List

from models.activity import Activity
from storage.json_storage import JsonStorage

'''
exapmle:
    input = AnalysisInput(activities)
    output = Analysis(input).output()
'''

class AnalysisInput(BaseModel):
    '''
    分析用のリクエストボディ
    '''
    activities: List[Activity]

class AnalysisOutput(BaseModel):
    '''
    分析結果のレスポンスボディ
    '''
    emotion_histgram: dict # 感情ごとの出現回数

class Analysis:
    def __init__(self, activities: List[Activity]):
        self.activities = activities

    def output(self) -> AnalysisOutput:
        output = AnalysisOutput()
        output.emotion_histgram = self.get_enotion_histgram()
        return output

    def get_enotion_histgram(self) -> dict:
        pass