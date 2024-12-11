import os
import re
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel  # , Field


# モデル設定クラス
class EmotionAnalyzer(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm = LlamaCpp(
            model_path=self.model_path,
            n_gpu_layers=self.n_gpu_layers,
        )
        self.question_prompt = PromptTemplate(
            input_variables=["statement"],
            template="""
                あなたは感情分析のエキスパートです。以下の出来事から想像される感情の種別を一つ
                の英単語で答えてください。回答は感情の英単語のみとしてください。\n{statement}
            """,
        )

    def analyze_emotion(self, statement: str) -> str:
        chain = self.question_prompt | self.llm
        response = chain.invoke({"statement": statement})
        filtered_text = re.sub(r"[^a-zA-Z0-9\s]", "", response)
        return filtered_text


# ファイルパスの取得と設定
def get_model_path() -> str:
    resources_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(resources_dir, "resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf")
    return file_path


if __name__ == "__main__":
    model_path = get_model_path()
    emotion_analyzer = EmotionAnalyzer(model_path=model_path)

    statement = "テストで100点を取ったが、父親が褒めてくれなかった"
    result = emotion_analyzer.analyze_emotion(statement)
    print(result)
