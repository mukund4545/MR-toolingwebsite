import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from models import Content, ContentUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from datetime import datetime, timezone
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/content", tags=["content"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[Content])
async def get_all_content():
    """Get all content"""
    try:
        from datetime import datetime
        content_list = await db.content.find({}, {"_id": 0}).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for content in content_list:
            if isinstance(content.get('updated_at'), str):
                content['updated_at'] = datetime.fromisoformat(content['updated_at'])
        return [Content(**content) for content in content_list]
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{content_type}", response_model=Content)
async def get_content_by_type(content_type: str):
    """Get specific content by type"""
    try:
        from datetime import datetime
        content = await db.content.find_one({"content_type": content_type}, {"_id": 0})
        if not content:
            raise HTTPException(status_code=404, detail=f"Content type '{content_type}' not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(content.get('updated_at'), str):
            content['updated_at'] = datetime.fromisoformat(content['updated_at'])
        return Content(**content)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{content_type}", response_model=Content, dependencies=[Depends(get_admin_user)])
async def update_content(content_type: str, content_update: ContentUpdate):
    """Update content (admin only)"""
    try:
        from datetime import datetime
        update_time = datetime.now(timezone.utc)
        result = await db.content.find_one_and_update(
            {"content_type": content_type},
            {"$set": {
                "content_data": content_update.content_data,
                "updated_at": update_time.isoformat()
            }},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail=f"Content type '{content_type}' not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('updated_at'), str):
            result['updated_at'] = datetime.fromisoformat(result['updated_at'])
        return Content(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))