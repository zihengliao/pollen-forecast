from apscheduler.schedulers.background import BackgroundScheduler
from app.services.google_pollen import fetch_and_cache_pollen

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_cache_pollen, "interval", minutes=10)
    scheduler.start()
