import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def restore_gallery_images():
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("Restoring uploaded gallery images...")

    # Get existing gallery images
    existing = await db.gallery_images.find({}, {'_id': 0}).to_list(100)
    print(f'Found {len(existing)} existing gallery images in database')

    # Check uploads directory
    uploads_dir = Path('uploads/gallery')
    if uploads_dir.exists():
        uploaded_files = list(uploads_dir.glob('*'))
        print(f'Found {len(uploaded_files)} uploaded files in uploads/gallery/')

        # Create gallery entries for uploaded files that don't exist
        now = datetime.now(timezone.utc).isoformat()
        order_start = len(existing) + 1

        restored_count = 0
        for i, file_path in enumerate(uploaded_files):
            filename = file_path.name
            url = f'/uploads/gallery/{filename}'

            # Check if this image already exists
            exists = any(img['url'] == url for img in existing)
            if not exists:
                # Extract title from filename (remove timestamp prefix)
                title_parts = filename.split('_', 2)
                if len(title_parts) >= 3:
                    title = title_parts[2].rsplit('.', 1)[0].replace('_', ' ').title()
                else:
                    title = filename.rsplit('.', 1)[0].replace('_', ' ').title()

                gallery_item = {
                    'id': f'restored_{i+1}',
                    'url': url,
                    'title': title,
                    'category': 'machinery',  # Default category
                    'order': order_start + i,
                    'active': True,
                    'created_at': now
                }

                await db.gallery_images.insert_one(gallery_item)
                print(f'✓ Restored: {title}')
                restored_count += 1

        print(f'Successfully restored {restored_count} gallery images')
    else:
        print('uploads/gallery directory not found')

    print('Gallery restoration completed')

if __name__ == "__main__":
    asyncio.run(restore_gallery_images())