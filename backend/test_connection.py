"""Quick test script to check MongoDB connection"""
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def test_connection():
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME')
        
        if not mongo_url:
            print("ERROR: MONGO_URL not found in environment variables")
            print("   Make sure .env file exists in backend/ folder")
            return False
        
        if not db_name:
            print("ERROR: DB_NAME not found in environment variables")
            return False
        
        print(f"Connecting to MongoDB...")
        print(f"   URL: {mongo_url[:50]}...")
        print(f"   Database: {db_name}")
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Test connection
        await client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"Collections: {collections if collections else 'None (database is empty)'}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("\nCommon issues:")
        print("1. MongoDB connection string is incorrect")
        print("2. IP address not whitelisted (for Atlas)")
        print("3. Username/password incorrect")
        print("4. Network connectivity issues")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    exit(0 if result else 1)

