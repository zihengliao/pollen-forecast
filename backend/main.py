from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.pollen import router as pollen_router
from scheduler.cron import start_scheduler

app = FastAPI()
start_scheduler()

# CORS so React can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pollen_router)

@app.get("/")
def root():
    return {"message": "FastAPI backend working!"}
