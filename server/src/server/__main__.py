import os
from dotenv import load_dotenv
from utils.lib import greet
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


if __name__ == "__main__":
    uvicorn.run(app)
