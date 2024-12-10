from utils.lib import greet
import uvicorn
from fastapi import FastAPI

from models.activity import Activity
from storage.json_storage import JsonStorage

from analysis.analysis import Analysis, AnalysisInput, AnalysisOutput, BaseOutput

app = FastAPI()

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
        "per_day": output.per_day.dict()
    }

if __name__ == "__main__":
    uvicorn.run(app)