from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from .config import settings


class Database:
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def get_database():
    """Get database instance"""
    return db.db


async def connect_to_mongo(database_name: Optional[str] = None):
    """Connect to MongoDB"""
    db_name = database_name or settings.DATABASE_NAME
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}, database: {db_name}...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
    db.db = db.client[db_name]
    
    # Verify connection
    try:
        await db.client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        db.db = None  # Ensure it's None so we can check it later
        raise e


async def close_mongo_connection():
    """Close MongoDB connection"""
    print("Closing MongoDB connection...")
    db.client.close()
    print("MongoDB connection closed!")


# Collections
def get_users_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.users


def get_reports_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.reports


def get_plans_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.plans


def get_meals_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.meals



def get_food_logs_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.food_logs


def get_disease_reports_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.disease_reports


def get_outbreak_alerts_collection():
    if db.db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db.db.outbreak_alerts
