import os
import logging
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from models import GalleryImage, GalleryImageCreate, GalleryImageUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from api.routes.auth import get_admin_user
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("", response_model=List[GalleryImage])
async def get_all_gallery_images():
    """Get all active gallery images"""
    try:
        from datetime import datetime
        images = await db.gallery_images.find({"active": True}, {"_id": 0}).sort("order", 1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for image in images:
            if isinstance(image.get('created_at'), str):
                image['created_at'] = datetime.fromisoformat(image['created_at'])
        return [GalleryImage(**image) for image in images]
    except Exception as e:
        logger.error(f"Error fetching gallery images: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=GalleryImage, dependencies=[Depends(get_admin_user)])
async def create_gallery_image(
    title: str = Form(...),
    category: str = Form("machinery"),
    order: str = Form("0"),  # Accept as string from FormData
    url: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None)
):
    """Add a new gallery image (admin only)"""
    try:
        from datetime import datetime, timezone
        
        # Convert order to int
        try:
            order_int = int(order)
        except ValueError:
            order_int = 0
        
        image_url = url.strip() if url else None
        if file and file.filename:
            # Save the uploaded file
            upload_dir = Path("uploads/gallery")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            file_extension = Path(file.filename).suffix
            unique_filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = upload_dir / unique_filename
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Create URL for the image
            image_url = f"/uploads/gallery/{unique_filename}"
        
        if not image_url:
            raise HTTPException(status_code=400, detail="Either URL or file must be provided")
        
        image_dict = {
            "url": image_url,
            "title": title,
            "category": category,
            "order": order_int,
            "active": True
        }
        image_obj = GalleryImage(**image_dict, created_at=datetime.now(timezone.utc))
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = image_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.gallery_images.insert_one(doc)
        return image_obj
    except Exception as e:
        logger.error(f"Error creating gallery image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        return image_obj
    except Exception as e:
        logger.error(f"Error creating gallery image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{image_id}", response_model=GalleryImage, dependencies=[Depends(get_admin_user)])
async def update_gallery_image(image_id: str, image_update: GalleryImageUpdate):
    """Update a gallery image (admin only)"""
    try:
        update_data = {k: v for k, v in image_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.gallery_images.find_one_and_update(
            {"id": image_id},
            {"$set": update_data},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Gallery image not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return GalleryImage(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating gallery image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{image_id}", dependencies=[Depends(get_admin_user)])
async def delete_gallery_image(image_id: str):
    """Delete a gallery image (admin only)"""
    try:
        result = await db.gallery_images.delete_one({"id": image_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Gallery image not found")
        return {"message": "Gallery image deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting gallery image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))