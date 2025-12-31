import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from models import Service, ServiceCreate, ServiceUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/services", tags=["services"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[Service])
async def get_all_services():
    """Get all active services"""
    try:
        from datetime import datetime
        services = await db.services.find({"active": True}, {"_id": 0}).sort("order", 1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for service in services:
            if isinstance(service.get('created_at'), str):
                service['created_at'] = datetime.fromisoformat(service['created_at'])
        return [Service(**service) for service in services]
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Service, dependencies=[Depends(get_admin_user)])
async def create_service(service: ServiceCreate):
    """Create a new service (admin only)"""
    try:
        from datetime import datetime, timezone
        service_dict = service.model_dump()
        service_obj = Service(**service_dict, created_at=datetime.now(timezone.utc))
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = service_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.services.insert_one(doc)
        return service_obj
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{service_id}", response_model=Service, dependencies=[Depends(get_admin_user)])
async def update_service(service_id: str, service_update: ServiceUpdate):
    """Update a service (admin only)"""
    try:
        update_data = {k: v for k, v in service_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.services.find_one_and_update(
            {"id": service_id},
            {"$set": update_data},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Service not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return Service(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{service_id}", dependencies=[Depends(get_admin_user)])
async def delete_service(service_id: str):
    """Delete a service (admin only)"""
    try:
        result = await db.services.delete_one({"id": service_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Service not found")
        return {"message": "Service deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))