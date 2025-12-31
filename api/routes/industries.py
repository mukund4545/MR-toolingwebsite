import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from api.models import Industry, IndustryCreate, IndustryUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/industries", tags=["industries"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[Industry])
async def get_all_industries():
    """Get all active industries"""
    try:
        from datetime import datetime
        industries = await db.industries.find({"active": True}, {"_id": 0}).sort("order", 1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for industry in industries:
            if isinstance(industry.get('created_at'), str):
                industry['created_at'] = datetime.fromisoformat(industry['created_at'])
        return [Industry(**industry) for industry in industries]
    except Exception as e:
        logger.error(f"Error fetching industries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Industry, dependencies=[Depends(get_admin_user)])
async def create_industry(industry: IndustryCreate):
    """Create a new industry (admin only)"""
    try:
        from datetime import datetime, timezone
        industry_dict = industry.model_dump()
        industry_obj = Industry(**industry_dict, created_at=datetime.now(timezone.utc))
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = industry_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.industries.insert_one(doc)
        return industry_obj
    except Exception as e:
        logger.error(f"Error creating industry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{industry_id}", response_model=Industry, dependencies=[Depends(get_admin_user)])
async def update_industry(industry_id: str, industry_update: IndustryUpdate):
    """Update an industry (admin only)"""
    try:
        update_data = {k: v for k, v in industry_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.industries.find_one_and_update(
            {"id": industry_id},
            {"$set": update_data},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Industry not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return Industry(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating industry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{industry_id}", dependencies=[Depends(get_admin_user)])
async def delete_industry(industry_id: str):
    """Delete an industry (admin only)"""
    try:
        result = await db.industries.delete_one({"id": industry_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Industry not found")
        return {"message": "Industry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting industry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))