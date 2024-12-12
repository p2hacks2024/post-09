# from langchain_community.llms import LlamaCpp
from langchain_community.chat_models import ChatLlamaCpp
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from models.activity import Music, Activity
from langchain_core.tools import tool


@tool
async def out_emotion(emotion: str) -> str:
    return "こんにちは～～～～～～うるせぇよ"


# Load the Llama model
model_path = "path/to/llama3.2.gguf"
llm = ChatLlamaCpp(
    model_path="/home/makebrain/ptwo/post-09/server/src/suggester/resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf",
    n_gpu_layers=-1,
    n_batch=512,
    verbose=True,
)


class EmotionAnalysis(BaseModel):
    """
    A result of emotion analysis from user input
    """

    comment: str = Field(
        description="""a comforting comment to user's episode 
        (e.g. What a sad story. I'm so sorry to here that.)"""
    )
    emotion: str = Field(
        description="emotion (e.g. angry)",
        examples=["sad", "angry", "dissapointed"],
        pattren=r"^[A-Za-z]+$",
    )
    summary: str = Field(
        description="a short summary of happening",
        examples=["友人との喧嘩", "仕事での失敗", "失恋"],
    )
    music_recommendation: str = Field(
        description="recommended music based on user prompt",
        examples=["Singing in the rain"],
    )


question_prompt = PromptTemplate(
    input_variables=["statement"],
    template="""
                あなたは感情分析のエキスパートです。以下はユーザーが体験した出来事です。
                また、出来事を一言で要約してください。
                次に、出来事に対するコメントを少し長めに書いてください。このコメントには、
                ユーザーに対する慰めも含めてください。
                次に、ユーザーの出来事に基づいて一つの曲名を書いてください。
                最後に、コメントを元にユーザーの感情を一つの英単語の形容詞で出力してください。
                (例： lonely, angry, happy, complex, envy anxious, fear)\n
                  {statement}
            """,
)


# ツールの定義 (感情に基づいて何かを行う)
def emotion_tool(emotion: str) -> str:
    if emotion == "sad":
        return "慰めの音楽を再生します。"
    elif emotion == "happy":
        return "楽しい活動を提案します！"
    return "感情を認識できませんでした。"


tool = Tool(
    name="Emotion Tool", func=emotion_tool, description="感情に基づいたツール呼び出し"
)

# エージェントを初期化 (Zero-shot反応型エージェント)
tools = [tool]
agent = initialize_agent(
    tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

structured_llm = llm.with_structured_output(EmotionAnalysis)


chain = question_prompt | structured_llm
response = chain.invoke(
    {"statement": "家で留守番をしているんだけど、ずっと誰も帰ってこないです"}
)

print(response)

# 感情を取り出してエージェントでツールを呼び出す
emotion = response.emotion
tool_response = agent.run(emotion)

# ツールの結果を表示
print(tool_response)
