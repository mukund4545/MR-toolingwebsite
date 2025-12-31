import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from models import Stat, StatUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/stats", tags=["stats"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[Stat])
async def get_all_stats():
    """Get all stats"""
    try:
        stats = await db.stats.find({}, {"_id": 0}).sort("order", 1).to_list(1000)
        return [Stat(**stat) for stat in stats]
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("", response_model=List[Stat], dependencies=[Depends(get_admin_user)])
async def update_stats(stats: List[StatUpdate]):
    """Update all stats (admin only)"""
    try:
        # Clear existing stats
        await db.stats.delete_many({})
        
        # Insert new stats
        stats_dicts = [Stat(**stat.model_dump()).model_dump() for stat in stats]
        await db.stats.insert_many(stats_dicts)
        
        # Return updated stats
        updated_stats = await db.stats.find({}, {"_id": 0}).sort("order", 1).to_list(1000)
        return [Stat(**stat) for stat in updated_stats]
    except Exception as e:
        logger.error(f"Error updating stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))