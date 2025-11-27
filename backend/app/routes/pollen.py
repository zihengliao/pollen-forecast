from fastapi import APIRouter
from app.services.google_pollen import fetch_google_pollen

router = APIRouter()

@router.get("/pollen")
def get_pollen():
    return fetch_google_pollen()
