# MR Tooling Industries - Backend Implementation Contracts

## Overview
This document outlines the backend implementation for replacing mock data with real database-driven functionality and email integration.

## Mock Data to Replace (from /app/frontend/src/mock.js)
1. Company Info (address, phone, email, location)
2. Services (3 services with features)
3. About Content (mission, vision, description)
4. Infrastructure (4 infrastructure items)
5. Industries (2 industry items)
6. Gallery Images (6 images with categories)
7. Stats (4 stat items)

## Database Models

### 1. ContentModel
- Field: content_type (home_hero, about_mission, about_vision, etc.)
- Field: content_data (JSON object with flexible schema)
- Purpose: Store all editable website content

### 2. ServiceModel
- Fields: id, title, description, icon, features (array), order, active
- Purpose: Manage service offerings

### 3. InfrastructureModel
- Fields: id, title, description, icon, order, active
- Purpose: Manage infrastructure/capability items

### 4. IndustryModel
- Fields: id, title, description, icon, clients (array), order, active
- Purpose: Manage industries served

### 5. GalleryImageModel
- Fields: id, url, title, category, order, active
- Purpose: Manage gallery images

### 6. ContactInquiryModel
- Fields: id, name, email, phone, subject, message, request_quote, status, created_at
- Purpose: Store contact form submissions

### 7. QuoteRequestModel
- Fields: id, name, company, email, phone, service_type, material_type, quantity, description, timeline, status, created_at
- Purpose: Store quote requests

### 8. StatsModel
- Fields: id, label, value, order
- Purpose: Manage homepage statistics

## API Endpoints

### Content Management APIs
- GET /api/content - Get all content
- GET /api/content/:type - Get specific content type
- PUT /api/content/:type - Update content (admin only)

### Services APIs
- GET /api/services - Get all services
- POST /api/services - Create service (admin only)
- PUT /api/services/:id - Update service (admin only)
- DELETE /api/services/:id - Delete service (admin only)

### Infrastructure APIs
- GET /api/infrastructure - Get all infrastructure items
- POST /api/infrastructure - Create item (admin only)
- PUT /api/infrastructure/:id - Update item (admin only)
- DELETE /api/infrastructure/:id - Delete item (admin only)

### Industries APIs
- GET /api/industries - Get all industries
- POST /api/industries - Create industry (admin only)
- PUT /api/industries/:id - Update industry (admin only)
- DELETE /api/industries/:id - Delete industry (admin only)

### Gallery APIs
- GET /api/gallery - Get all gallery images
- POST /api/gallery - Add image (admin only)
- PUT /api/gallery/:id - Update image (admin only)
- DELETE /api/gallery/:id - Delete image (admin only)

### Stats APIs
- GET /api/stats - Get all stats
- PUT /api/stats - Update all stats (admin only)

### Contact APIs
- POST /api/contact - Submit contact form (sends email)
- GET /api/contact/inquiries - Get all inquiries (admin only)
- PUT /api/contact/inquiries/:id - Update inquiry status (admin only)

### Quote APIs
- POST /api/quote - Submit quote request (sends email)
- GET /api/quote/requests - Get all requests (admin only)
- PUT /api/quote/requests/:id - Update request status (admin only)

### Email Integration
- Use Resend API for sending emails
- Send to: mukundprajapati2408@gmail.com
- Templates: Contact inquiry, Quote request

## Frontend Integration Changes

### Replace mock.js imports with API calls:
1. Home page: Fetch services, stats, company info
2. About page: Fetch about content
3. Services page: Fetch services
4. Infrastructure page: Fetch infrastructure items
5. Gallery page: Fetch gallery images
6. Industries page: Fetch industries
7. Contact page: Submit contact form via API
8. Quote page: Submit quote request via API

### Create new frontend components:
1. Admin Panel (/admin route)
   - Login (simple password protection)
   - Content editor
   - Service/Infrastructure/Industry management
   - Gallery management
   - View inquiries and quotes

## Implementation Order
1. ✅ Frontend with mock data (COMPLETED)
2. Add Resend API key to .env
3. Install resend package
4. Create database models
5. Seed database with initial data from mock.js
6. Create backend APIs
7. Update frontend to use APIs
8. Create admin panel
9. Test email functionality
10. Test full flow

## Email Templates

### Contact Inquiry Email
Subject: New Contact Inquiry from [Name]
Body:
- Name: [name]
- Email: [email]
- Phone: [phone]
- Subject: [subject]
- Message: [message]
- Request Quote: [yes/no]

### Quote Request Email
Subject: New Quote Request from [Name]
Body:
- Name: [name]
- Company: [company]
- Email: [email]
- Phone: [phone]
- Service: [service_type]
- Material: [material_type]
- Quantity: [quantity]
- Timeline: [timeline]
- Description: [description]

## Admin Panel Features
1. Dashboard (inquiries count, quotes count)
2. Content Management (edit all text content)
3. Services Management (CRUD)
4. Infrastructure Management (CRUD)
5. Industries Management (CRUD)
6. Gallery Management (CRUD)
7. Stats Management (update values)
8. View & Manage Inquiries
9. View & Manage Quote Requests
