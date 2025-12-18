import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from datetime import datetime

from database import Database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

db = Database()

def cleanup_memory_job():
    try:
        logger.info("Starting memory cleanup...")
        db.cleanup_memory()
        logger.info("Memory cleanup completed")
    except Exception as e:
        logger.error(f"Memory cleanup error: {e}")

def cleanup_inactive_users_job():
    try:
        logger.info("Starting inactive users cleanup...")
        db.cleanup_inactive_users()
        logger.info("Inactive users cleanup completed")
    except Exception as e:
        logger.error(f"Inactive users cleanup error: {e}")

def health_check():
    logger.info(f"Scheduler health check - {datetime.utcnow().isoformat()}")

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone=pytz.UTC)
    
    scheduler.add_job(
        func=cleanup_memory_job,
        trigger="interval",
        minutes=30,
        id="cleanup_memory",
        replace_existing=True
    )
    
    scheduler.add_job(
        func=cleanup_inactive_users_job,
        trigger="interval",
        hours=24,
        id="cleanup_inactive_users",
        replace_existing=True
    )
    
    scheduler.add_job(
        func=health_check,
        trigger="interval",
        minutes=5,
        id="health_check",
        replace_existing=True
    )
    
    logger.info("Scheduler worker starting...")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler worker shutting down...")
        scheduler.shutdown()
