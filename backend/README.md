# Backend API Documentation

This is the FastAPI backend for the MR Tooling Industries website.

## Features

✅ **Complete REST API** with all endpoints  
✅ **Email functionality** using Resend API  
✅ **Admin authentication** with JWT tokens  
✅ **Database integration** with MongoDB  
✅ **Full CRUD operations** for all content types

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the `backend` directory:

```env
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=emergent_mr

# Resend API Configuration
RESEND_API_KEY=re_3r6xtssc_9nn5KE3qnR9AZrGQqinZg4Wn
SENDER_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=mukundprajapati2408@gmail.com

# JWT Secret Key (Change this in production!)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Admin Credentials (Change these in production!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Seed Database

Run the seed script to populate the database with initial data:

```bash
python seed_data.py
```

### 4. Run the Server

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Public Endpoints

#### Content
- `GET /api/content` - Get all content
- `GET /api/content/{content_type}` - Get specific content by type

#### Services
- `GET /api/services` - Get all active services

#### Infrastructure
- `GET /api/infrastructure` - Get all active infrastructure items

#### Industries
- `GET /api/industries` - Get all active industries

#### Gallery
- `GET /api/gallery` - Get all active gallery images

#### Stats
- `GET /api/stats` - Get all stats

#### Contact
- `POST /api/contact` - Submit contact form (sends email)

#### Quote
- `POST /api/quote` - Submit quote request (sends email)

### Admin Endpoints (Require Authentication)

#### Authentication
- `POST /api/auth/login` - Login and get JWT token
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- `GET /api/auth/me` - Get current user info (requires Bearer token)
- `POST /api/auth/change-password` - Change password (requires Bearer token)
  ```json
  {
    "old_password": "admin123",
    "new_password": "newpassword"
  }
  ```

#### Services (Admin)
- `POST /api/services` - Create new service
- `PUT /api/services/{service_id}` - Update service
- `DELETE /api/services/{service_id}` - Delete service

#### Content (Admin)
- `PUT /api/content/{content_type}` - Update content

#### Gallery (Admin)
- `POST /api/gallery` - Add gallery image
- `PUT /api/gallery/{image_id}` - Update gallery image
- `DELETE /api/gallery/{image_id}` - Delete gallery image

#### Industries (Admin)
- `POST /api/industries` - Create industry
- `PUT /api/industries/{industry_id}` - Update industry
- `DELETE /api/industries/{industry_id}` - Delete industry

#### Infrastructure (Admin)
- `POST /api/infrastructure` - Create infrastructure item
- `PUT /api/infrastructure/{infra_id}` - Update infrastructure item
- `DELETE /api/infrastructure/{infra_id}` - Delete infrastructure item

#### Stats (Admin)
- `PUT /api/stats` - Update all stats

#### Contact Inquiries (Admin)
- `GET /api/contact/inquiries` - Get all contact inquiries
- `PUT /api/contact/inquiries/{inquiry_id}` - Update inquiry status

#### Quote Requests (Admin)
- `GET /api/quote/requests` - Get all quote requests
- `PUT /api/quote/requests/{request_id}` - Update quote request status

## Authentication

All admin endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

1. Login at `POST /api/auth/login` with admin credentials
2. Copy the `access_token` from the response
3. Include it in all admin requests as shown above

## Email Configuration

The backend uses Resend API to send emails. When a contact form or quote request is submitted:

1. The data is saved to MongoDB
2. An email is automatically sent to `RECIPIENT_EMAIL` (mukundprajapati2408@gmail.com)

### Email Templates

- **Contact Inquiry**: Includes name, email, phone, subject, message, and quote request status
- **Quote Request**: Includes contact info, service type, material, quantity, timeline, and description

## Database Collections

- `content` - Company information and about page content
- `services` - Services offered
- `infrastructure` - Infrastructure capabilities
- `industries` - Industries served
- `gallery_images` - Gallery images
- `stats` - Statistics displayed on homepage
- `contact_inquiries` - Contact form submissions
- `quote_requests` - Quote request submissions
- `admin_users` - Admin user accounts

## Notes

- All datetime fields are stored as ISO format strings in MongoDB
- Admin user is automatically created on first login with default credentials
- Change admin credentials in production!
- Update JWT_SECRET_KEY in production for security



