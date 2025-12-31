import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from models import Infrastructure, InfrastructureCreate, InfrastructureUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/infrastructure", tags=["infrastructure"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[Infrastructure])
async def get_all_infrastructure():
    """Get all active infrastructure items"""
    try:
        from datetime import datetime
        infrastructure = await db.infrastructure.find({"active": True}, {"_id": 0}).sort("order", 1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for item in infrastructure:
            if isinstance(item.get('created_at'), str):
                item['created_at'] = datetime.fromisoformat(item['created_at'])
        return [Infrastructure(**item) for item in infrastructure]
    except Exception as e:
        logger.error(f"Error fetching infrastructure: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Infrastructure, dependencies=[Depends(get_admin_user)])
async def create_infrastructure(infrastructure: InfrastructureCreate):
    """Create a new infrastructure item (admin only)"""
    try:
        from datetime import datetime, timezone
        infra_dict = infrastructure.model_dump()
        infra_obj = Infrastructure(**infra_dict, created_at=datetime.now(timezone.utc))
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = infra_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.infrastructure.insert_one(doc)
        return infra_obj
    except Exception as e:
        logger.error(f"Error creating infrastructure: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{infra_id}", response_model=Infrastructure, dependencies=[Depends(get_admin_user)])
async def update_infrastructure(infra_id: str, infra_update: InfrastructureUpdate):
    """Update an infrastructure item (admin only)"""
    try:
        update_data = {k: v for k, v in infra_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.infrastructure.find_one_and_update(
            {"id": infra_id},
            {"$set": update_data},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Infrastructure item not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return Infrastructure(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating infrastructure: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{infra_id}", dependencies=[Depends(get_admin_user)])
async def delete_infrastructure(infra_id: str):
    """Delete an infrastructure item (admin only)"""
    try:
        result = await db.infrastructure.delete_one({"id": infra_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Infrastructure item not found")
        return {"message": "Infrastructure item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting infrastructure: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))