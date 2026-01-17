import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def update_gallery_urls():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    # Get all gallery images
    images = await db.gallery_images.find({}, {"_id": 0}).to_list(1000)

    for image in images:
        # Get the filename from the current url
        current_url = image['url']
        if current_url.startswith('/uploads/gallery/'):
            filename = current_url.split('/')[-1]
        elif current_url.startswith('http'):
            # If it's already a URL, skip or handle
            continue
        else:
            filename = current_url
        
        new_url = f"/gallery/{filename}"
        await db.gallery_images.update_one(
            {"id": image["id"]},
            {"$set": {"url": new_url}}
        )
        print(f"Updated {image['id']}: {new_url}")

    print("Gallery URLs updated")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_gallery_urls())