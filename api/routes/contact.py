import os
import asyncio
import logging
import resend
from fastapi import APIRouter, HTTPException, Depends
from models import ContactInquiryCreate, ContactInquiry, ContactInquiryStatusUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contact", tags=["contact"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Resend configuration
resend.api_key = os.environ.get('RESEND_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'mukundprajapati2408@gmail.com')

@router.post("", response_model=ContactInquiry)
async def submit_contact_form(inquiry: ContactInquiryCreate):
    """Submit a contact form inquiry and send email notification"""
    try:
        # Create inquiry object
        inquiry_dict = inquiry.model_dump()
        inquiry_obj = ContactInquiry(**inquiry_dict)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = inquiry_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        
        # Save to database
        await db.contact_inquiries.insert_one(doc)
        logger.info(f"Contact inquiry saved: {inquiry_obj.id}")
        
        # Prepare email content
        email_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                        New Contact Inquiry from Website
                    </h2>
                    
                    <div style="margin: 20px 0;">
                        <p><strong>Name:</strong> {inquiry_obj.name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{inquiry_obj.email}">{inquiry_obj.email}</a></p>
                        <p><strong>Phone:</strong> {inquiry_obj.phone or 'Not provided'}</p>
                        <p><strong>Subject:</strong> {inquiry_obj.subject}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Message:</strong></p>
                        <p style="white-space: pre-wrap;">{inquiry_obj.message}</p>
                    </div>
                    
                    <div style="margin: 20px 0; padding: 10px; background: {'#dbeafe' if inquiry_obj.request_quote else '#f3f4f6'}; border-radius: 5px;">
                        <p><strong>Quote Request:</strong> {'✓ Yes - Customer also wants a quote' if inquiry_obj.request_quote else '✗ No'}</p>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                        <p>This inquiry was submitted on {inquiry_obj.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p>Inquiry ID: {inquiry_obj.id}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send email using Resend
        params = {
            "from": SENDER_EMAIL,
            "to": [RECIPIENT_EMAIL],
            "subject": f"New Contact Inquiry: {inquiry_obj.subject}",
            "html": email_html
        }
        
        # Run sync SDK in thread to keep FastAPI non-blocking
        email_result = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Email sent successfully: {email_result.get('id')}")
        
        return inquiry_obj
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process inquiry: {str(e)}")

@router.get("/inquiries", response_model=List[ContactInquiry], dependencies=[Depends(get_admin_user)])
async def get_all_inquiries():
    """Get all contact inquiries (admin only)"""
    try:
        from datetime import datetime
        inquiries = await db.contact_inquiries.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for inquiry in inquiries:
            if isinstance(inquiry.get('created_at'), str):
                inquiry['created_at'] = datetime.fromisoformat(inquiry['created_at'])
        return [ContactInquiry(**inquiry) for inquiry in inquiries]
    except Exception as e:
        logger.error(f"Error fetching inquiries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/inquiries/{inquiry_id}", response_model=ContactInquiry, dependencies=[Depends(get_admin_user)])
async def update_inquiry_status(inquiry_id: str, status_update: ContactInquiryStatusUpdate):
    """Update inquiry status (admin only)"""
    try:
        result = await db.contact_inquiries.find_one_and_update(
            {"id": inquiry_id},
            {"$set": {"status": status_update.status}},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Inquiry not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return ContactInquiry(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating inquiry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))