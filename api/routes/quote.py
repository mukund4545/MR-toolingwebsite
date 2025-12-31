import os
import asyncio
import logging
import resend
from fastapi import APIRouter, HTTPException, Depends
from models import QuoteRequestCreate, QuoteRequest, QuoteRequestStatusUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from api.routes.auth import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/quote", tags=["quote"])

# Database connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Resend configuration
resend.api_key = os.environ.get('RESEND_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'mrtooling@hotmail.com')

@router.post("", response_model=QuoteRequest)
async def submit_quote_request(quote: QuoteRequestCreate):
    """Submit a quote request and send email notification"""
    try:
        # Create quote request object
        quote_dict = quote.model_dump()
        quote_obj = QuoteRequest(**quote_dict)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = quote_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        
        # Save to database
        await db.quote_requests.insert_one(doc)
        logger.info(f"Quote request saved: {quote_obj.id}")
        
        # Prepare email content
        email_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                        New Quote Request from Website
                    </h2>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #1f2937;">Contact Information</h3>
                        <p><strong>Name:</strong> {quote_obj.name}</p>
                        <p><strong>Company:</strong> {quote_obj.company or 'Not provided'}</p>
                        <p><strong>Email:</strong> <a href="mailto:{quote_obj.email}">{quote_obj.email}</a></p>
                        <p><strong>Phone:</strong> {quote_obj.phone}</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #1f2937;">Project Details</h3>
                        <p><strong>Service Type:</strong> {quote_obj.service_type}</p>
                        <p><strong>Material Type:</strong> {quote_obj.material_type or 'Not specified'}</p>
                        <p><strong>Estimated Quantity:</strong> {quote_obj.quantity}</p>
                        <p><strong>Expected Timeline:</strong> {quote_obj.timeline or 'Not specified'}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Project Description:</strong></p>
                        <p style="white-space: pre-wrap;">{quote_obj.description}</p>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                        <p>This quote request was submitted on {quote_obj.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p>Request ID: {quote_obj.id}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send email using Resend
        params = {
            "from": SENDER_EMAIL,
            "to": [RECIPIENT_EMAIL],
            "subject": f"New Quote Request from {quote_obj.name} - {quote_obj.service_type}",
            "html": email_html
        }
        
        # Run sync SDK in thread to keep FastAPI non-blocking
        email_result = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Email sent successfully: {email_result.get('id')}")
        
        return quote_obj
        
    except Exception as e:
        logger.error(f"Error processing quote request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process quote request: {str(e)}")

@router.get("/requests", response_model=List[QuoteRequest], dependencies=[Depends(get_admin_user)])
async def get_all_quote_requests():
    """Get all quote requests (admin only)"""
    try:
        from datetime import datetime
        requests = await db.quote_requests.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        # Convert ISO string timestamps back to datetime objects
        for req in requests:
            if isinstance(req.get('created_at'), str):
                req['created_at'] = datetime.fromisoformat(req['created_at'])
        return [QuoteRequest(**req) for req in requests]
    except Exception as e:
        logger.error(f"Error fetching quote requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/requests/{request_id}", response_model=QuoteRequest, dependencies=[Depends(get_admin_user)])
async def update_quote_request_status(request_id: str, status_update: QuoteRequestStatusUpdate):
    """Update quote request status (admin only)"""
    try:
        result = await db.quote_requests.find_one_and_update(
            {"id": request_id},
            {"$set": {"status": status_update.status}},
            return_document=True,
            projection={"_id": 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Quote request not found")
        # Convert ISO string timestamp back to datetime object
        if isinstance(result.get('created_at'), str):
            from datetime import datetime
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return QuoteRequest(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating quote request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))