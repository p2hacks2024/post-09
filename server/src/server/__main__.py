import os
from dotenv import load_dotenv
from pydantic import BaseModel
from models.activity import Activity
from utils.lib import greet  # pyright:ignore
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from storage.json_storage import JsonStorage  # pyright:ignore
from analysis.analysis import Analysis, AnalysisInput
from suggester.suggester_models import SuggesterInput, SuggesterOutput
from suggester.suggester_core import Suggester
from datetime import datetime

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
    storage = JsonStorage("test_data/test_activities.json")
    activities = storage.read_user_activities(user_id)
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


# llm server: returns SuggesterOutput after writing db
@app.post("/suggester/{user_id}", response_model=SuggesterOutput)
async def suggester(user_id: str, api_input: SuggesterRequest) -> SuggesterOutput:
    # load db
    storage = JsonStorage("test_data/test_activities.json")
    activities = storage.read_user_activities(user_id)

    # run llm
    input = SuggesterInput(
        emotion=api_input.emotion, prompt=api_input.prompt, activities=activities
    )
    suggester = Suggester(input=input)
    output = suggester.llm_runner()
    # write db
    activity_this_time = Activity(
        timestamp=str(datetime.now().replace(microsecond=0).isoformat()),
        prompt=api_input.prompt,
        emotion=output.emotion,
        situation=output.summary,
        musics=output.musics,
    )
    storage.update_user_activities(user_id, [activity_this_time])

    return output


if __name__ == "__main__":
    uvicorn.run(app)
