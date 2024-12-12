from pyexpat import model
from attrs import field
from langchain_community.llms import LlamaCpp
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from models.activity import Music, Activity

# Load the Llama model
model_path = "path/to/llama3.2.gguf"
llm = LlamaCpp(
    model_path="/home/makebrain/ptwo/post-09/server/src/suggester/resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf",
    n_gpu_layers=-1,
    n_batch=512,
    verbose=True,
)


class EmotionAnalysis(BaseModel):
    # comment: str = Field(
    #     description="a comforting comment to user's episode (e.g. What a sad story. I'm so sorry to here that.)"
    # )
    emotion: str = Field(description="emotion (e.g. sad, angry, disgusting)")
    summary: str = Field(description="a short summary of happening")


parser = PydanticOutputParser(pydantic_object=EmotionAnalysis)

question_prompt = PromptTemplate(
    input_variables=["statement"],
    template="""
                あなたは感情分析のエキスパートです。以下はユーザーが体験した出来事です。\n{format_instructions}\n{statement}\n
            """,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = question_prompt | llm | parser
response = chain.invoke(
    {
        "statement": "母親に「あなたはうちの子じゃないと言われた」。父親にも似たようなことを言われたあと、おじいちゃんにも「お前と血のつながりがあるのは恥だ」と言われました。"
    }
)

print(response)
