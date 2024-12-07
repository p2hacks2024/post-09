from utils.lib import greet
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": greet()}

if __name__ == "__main__":
    uvicorn.run(app)