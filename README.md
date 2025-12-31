# MR Tooling Industries - Website

A complete website for MR Tooling Industries with frontend, backend, and admin panel.

## Features

### Public Website
- ✅ Home page with hero, services overview, stats, and CTA
- ✅ About Us page with mission, vision, and core values
- ✅ Services page with detailed descriptions
- ✅ Infrastructure page showcasing capabilities
- ✅ Gallery with filtering (machinery, products, facility)
- ✅ Industries page (Automotive & Industrial sectors)
- ✅ Contact page with form and Google Maps
- ✅ Request Quote page with detailed form

### Admin Panel
- ✅ Secure authentication with JWT
- ✅ Dashboard with statistics
- ✅ Content management (company info, about page)
- ✅ Services management (CRUD)
- ✅ Infrastructure management (CRUD)
- ✅ Industries management (CRUD)
- ✅ Gallery management (CRUD)
- ✅ Stats management
- ✅ View and manage contact inquiries
- ✅ View and manage quote requests

### Backend API
- ✅ RESTful API with FastAPI
- ✅ MongoDB database integration
- ✅ Email functionality via Resend API
- ✅ JWT authentication
- ✅ CORS enabled
- ✅ Complete CRUD operations

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```



3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Seed the database:
```bash
python seed_data.py
```

5. Run the server:
```bash
uvicorn server:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

4. Start development server:
```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## Project Structure

```
emergent-mr/
├── backend/
│   ├── routes/          # API route handlers
│   ├── models.py        # Pydantic models
│   ├── server.py        # FastAPI application
│   ├── seed_data.py     # Database seeding script
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API service layer
│   │   └── App.js       # Main app component
│   └── package.json     # Node dependencies
└── README.md
```

## Admin Access

Default admin credentials:
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT:** Change these credentials in production!

## API Endpoints

### Public Endpoints
- `GET /api/content` - Get all content
- `GET /api/services` - Get all services
- `GET /api/infrastructure` - Get infrastructure items
- `GET /api/industries` - Get industries
- `GET /api/gallery` - Get gallery images
- `GET /api/stats` - Get statistics
- `POST /api/contact` - Submit contact form
- `POST /api/quote` - Submit quote request

### Admin Endpoints (Require Authentication)
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- All CRUD operations for content management

See `backend/README.md` for complete API documentation.

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions.

## Technology Stack

### Frontend
- React 18
- React Router 6
- Tailwind CSS
- Axios
- Lucide React Icons

### Backend
- FastAPI
- MongoDB (Motor async driver)
- Resend (Email service)
- JWT (Authentication)
- Pydantic (Data validation)

## License

Proprietary - All rights reserved




