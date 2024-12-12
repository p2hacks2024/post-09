import os
from dotenv import load_dotenv
from pydantic import BaseModel
from utils.lib import greet  # pyright:ignore
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from storage.json_storage import JsonStorage  # pyright:ignore
from analysis.analysis import Analysis, AnalysisInput, AnalysisOutput, BaseOutput
from suggester.suggester_models import SuggesterInput, SuggesterOutput
from analysis.analysis import Analysis, AnalysisInput  # pyright:ignore
from suggester.suggester_core import Suggester  # pyright:ignore

app = FastAPI()

load_dotenv(verbose=True)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(os.environ.get("FRONTEND_ORIGIN"))],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": greet()}


@app.post("/analysis/{user_id}")
async def analysis(user_id: str):
    storge = JsonStorage("test_data/test_activities.json")
    activities = storge.read_user_activities(user_id)
    input = AnalysisInput(activities=activities)
    output = Analysis(input).output()
    return {
        "per_total": output.per_total.model_dump(),
        "per_year": output.per_year.model_dump(),
        "per_month": output.per_month.model_dump(),
        "per_week": output.per_week.model_dump(),
        "per_day": output.per_day.model_dump(),
    }


class SuggesterRequest(BaseModel):
    emotion: str
    prompt: str


# LLMサーバー
@app.post("/suggester/{user_id}", response_model=SuggesterOutput)
async def suggester(user_id: str, api_input: SuggesterRequest) -> SuggesterOutput:
    storge = JsonStorage("test_data/test_activities.json")
    activities = storge.read_user_activities(user_id)
    input = SuggesterInput(
        emotion=api_input.emotion, prompt=api_input.prompt, activities=activities
    )
    suggester = Suggester(input=input)
    output = suggester.llm_runner()
    return output


if __name__ == "__main__":
    uvicorn.run(app)
