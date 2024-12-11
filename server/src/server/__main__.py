import os
from dotenv import load_dotenv
from utils.lib import greet
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.activity import Activity
from storage.json_storage import JsonStorage

from analysis.analysis import Analysis, AnalysisInput, AnalysisOutput, BaseOutput
from suggester.suggester import Suggester, SuggesterInput, SuggesterOutput

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
        "per_total": output.per_total.dict(),
        "per_year": output.per_year.dict(),
        "per_month": output.per_month.dict(),
        "per_week": output.per_week.dict(),
        "per_day": output.per_day.dict(),
    }


@app.post("/suggester", response_model=SuggesterOutput)
async def suggester(input: SuggesterInput) -> SuggesterOutput:
    suggester = Suggester(input=input)
    output = suggester.llm_runner()
    return output


if __name__ == "__main__":
    uvicorn.run(app)
