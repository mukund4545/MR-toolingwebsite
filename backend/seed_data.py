import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def seed_database():
    from datetime import datetime, timezone
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Seeding database with initial data...")
    
    # Clear existing data
    await db.content.delete_many({})
    await db.services.delete_many({})
    await db.infrastructure.delete_many({})
    await db.industries.delete_many({})
    await db.gallery_images.delete_many({})
    await db.stats.delete_many({})
    
    # Seed Company Info Content
    company_info = {
        "id": "company_info",
        "content_type": "company_info",
        "content_data": {
            "name": "MR Tooling Industries",
            "tagline": "Excellence in Plastic Injection Molding & Automotive Components",
            "address": "Plot No-PAP-A-54/2, Behind HP Petrol Pump, Opp. Mahindra Company, Nighoje, Maharashtra 410501",
            "phone": "+91 9422005728",
            "email": "mukundprajapati2408@gmail.com",
            "mapLocation": {
                "lat": 18.6298,
                "lng": 73.7997
            }
        },
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    await db.content.insert_one(company_info)
    print("Company info seeded")
    
    # Seed About Content
    about_content = {
        "id": "about_content",
        "content_type": "about_content",
        "content_data": {
            "mission": "To deliver world-class plastic injection molding solutions that exceed customer expectations through innovation, quality, and reliability.",
            "vision": "To be the most trusted partner in plastic component manufacturing for automotive and industrial sectors across India.",
            "experience": "15+ Years",
            "description": "MR Tooling Industries is a leading plastic injection molding workshop based in Maharashtra, India. With over 15 years of expertise in manufacturing high-quality plastic components and automobile parts, we have established ourselves as a trusted partner for industrial and automotive applications. Our state-of-the-art facility is equipped with modern machinery and operated by skilled professionals committed to excellence."
        },
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    await db.content.insert_one(about_content)
    print("About content seeded")
    
    # Seed Services
    now = datetime.now(timezone.utc).isoformat()
    services = [
        {
            "id": "service_1",
            "title": "Plastic Injection Molding",
            "description": "High-precision plastic injection molding services for complex components with tight tolerances. We utilize state-of-the-art machinery to deliver consistent quality.",
            "icon": "factory",
            "features": ["High Precision", "Fast Turnaround", "Quality Assured", "Cost Effective"],
            "order": 1,
            "active": True,
            "created_at": now
        },
        {
            "id": "service_2",
            "title": "Plastic Components",
            "description": "Custom plastic component manufacturing for industrial applications. From prototyping to mass production, we handle all your plastic manufacturing needs.",
            "icon": "package",
            "features": ["Custom Solutions", "Prototyping", "Mass Production", "Quality Control"],
            "order": 2,
            "active": True,
            "created_at": now
        },
        {
            "id": "service_3",
            "title": "Automotive Components",
            "description": "Specialized in manufacturing high-quality automotive plastic components meeting international standards for leading automobile manufacturers.",
            "icon": "car",
            "features": ["OEM Standards", "Durability Tested", "Certified Quality", "Timely Delivery"],
            "order": 3,
            "active": True,
            "created_at": now
        }
    ]
    await db.services.insert_many(services)
    print("Services seeded")
    
    # Seed Infrastructure
    infrastructure = [
        {
            "id": "infra_1",
            "title": "Modern Machinery",
            "description": "Equipped with latest injection molding machines ranging from 50 to 500 tons",
            "icon": "settings",
            "order": 1,
            "active": True,
            "created_at": now
        },
        {
            "id": "infra_2",
            "title": "Quality Control Lab",
            "description": "In-house quality testing facility ensuring every component meets specifications",
            "icon": "shield-check",
            "order": 2,
            "active": True,
            "created_at": now
        },
        {
            "id": "infra_3",
            "title": "Skilled Workforce",
            "description": "Team of experienced engineers and technicians dedicated to precision",
            "icon": "users",
            "order": 3,
            "active": True,
            "created_at": now
        },
        {
            "id": "infra_4",
            "title": "ISO Certified",
            "description": "ISO 9001:2015 certified manufacturing processes and quality systems",
            "icon": "award",
            "order": 4,
            "active": True,
            "created_at": now
        }
    ]
    await db.infrastructure.insert_many(infrastructure)
    print("Infrastructure seeded")
    
    # Seed Industries
    industries = [
        {
            "id": "industry_1",
            "title": "Automotive Industry",
            "description": "Manufacturing precision automotive components for leading vehicle manufacturers including interior parts, exterior trims, and under-the-hood components.",
            "icon": "car",
            "clients": ["Passenger Vehicles", "Commercial Vehicles", "Two Wheelers"],
            "order": 1,
            "active": True,
            "created_at": now
        },
        {
            "id": "industry_2",
            "title": "Industrial Sector",
            "description": "Providing durable plastic components for industrial machinery, electrical appliances, and consumer goods manufacturing.",
            "icon": "building",
            "clients": ["Manufacturing Units", "Electrical Industry", "Consumer Goods"],
            "order": 2,
            "active": True,
            "created_at": now
        }
    ]
    await db.industries.insert_many(industries)
    print("Industries seeded")
    
    # Seed Gallery Images
    gallery_images = [
        {
            "id": "gallery_1",
            "url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80",
            "title": "Injection Molding Machine",
            "category": "machinery",
            "order": 1,
            "active": True,
            "created_at": now
        },
        {
            "id": "gallery_2",
            "url": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80",
            "title": "Automotive Components",
            "category": "products",
            "order": 2,
            "active": True,
            "created_at": now
        },
        {
            "id": "gallery_3",
            "url": "https://images.unsplash.com/photo-1565106430482-8f6e74349ca1?w=800&q=80",
            "title": "Quality Control",
            "category": "facility",
            "order": 3,
            "active": True,
            "created_at": now
        },
        {
            "id": "gallery_4",
            "url": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&q=80",
            "title": "Manufacturing Floor",
            "category": "facility",
            "order": 4,
            "active": True,
            "created_at": now
        },
        {
            "id": "gallery_5",
            "url": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&q=80",
            "title": "Plastic Components",
            "category": "products",
            "order": 5,
            "active": True,
            "created_at": now
        },
        {
            "id": "gallery_6",
            "url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80",
            "title": "Workshop Area",
            "category": "facility",
            "order": 6,
            "active": True,
            "created_at": now
        }
    ]
    await db.gallery_images.insert_many(gallery_images)
    print("Gallery images seeded")
    
    # Seed Stats
    stats = [
        {"id": "stat_1", "label": "Years Experience", "value": "15+", "order": 1},
        {"id": "stat_2", "label": "Happy Clients", "value": "200+", "order": 2},
        {"id": "stat_3", "label": "Projects Completed", "value": "5000+", "order": 3},
        {"id": "stat_4", "label": "Team Members", "value": "50+", "order": 4}
    ]
    await db.stats.insert_many(stats)
    print("Stats seeded")
    
    print("Database seeding completed successfully!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
