from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

# Helper function for generating IDs
def generate_id():
    return str(uuid.uuid4())

# Content Model for flexible content management
class Content(BaseModel):
    id: str = Field(default_factory=generate_id)
    content_type: str  # e.g., 'company_info', 'about_mission', 'about_vision'
    content_data: Dict[str, Any]  # Flexible JSON data
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContentUpdate(BaseModel):
    content_data: Dict[str, Any]

# Service Model
class Service(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str
    icon: str
    features: List[str]
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ServiceCreate(BaseModel):
    title: str
    description: str
    icon: str
    features: List[str]
    order: int = 0

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    features: Optional[List[str]] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Infrastructure Model
class Infrastructure(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str
    icon: str
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InfrastructureCreate(BaseModel):
    title: str
    description: str
    icon: str
    order: int = 0

class InfrastructureUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Industry Model
class Industry(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str
    icon: str
    clients: List[str]
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class IndustryCreate(BaseModel):
    title: str
    description: str
    icon: str
    clients: List[str]
    order: int = 0

class IndustryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    clients: Optional[List[str]] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Gallery Image Model
class GalleryImage(BaseModel):
    id: str = Field(default_factory=generate_id)
    url: str
    title: str
    category: str  # machinery, products, facility
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GalleryImageCreate(BaseModel):
    url: str
    title: str
    category: str
    order: int = 0

class GalleryImageUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Stats Model
class Stat(BaseModel):
    id: str = Field(default_factory=generate_id)
    label: str
    value: str
    order: int = 0

class StatUpdate(BaseModel):
    label: str
    value: str
    order: int

# Contact Inquiry Model
class ContactInquiry(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    request_quote: bool = False
    status: str = "new"  # new, read, contacted, closed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactInquiryCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    request_quote: bool = False

class ContactInquiryStatusUpdate(BaseModel):
    status: str

# Quote Request Model
class QuoteRequest(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    company: Optional[str] = None
    email: EmailStr
    phone: str
    service_type: str
    material_type: Optional[str] = None
    quantity: str
    description: str
    timeline: Optional[str] = None
    status: str = "new"  # new, reviewed, quoted, closed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuoteRequestCreate(BaseModel):
    name: str
    company: Optional[str] = None
    email: EmailStr
    phone: str
    service_type: str
    material_type: Optional[str] = None
    quantity: str
    description: str
    timeline: Optional[str] = None

class QuoteRequestStatusUpdate(BaseModel):
    status: str