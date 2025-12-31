# Deployment Guide

This guide will help you deploy the MR Tooling Industries website to production.

## Prerequisites

- Node.js 16+ and npm/yarn
- Python 3.8+
- MongoDB database (MongoDB Atlas recommended for production)
- Resend API account with API key
- Web server (Nginx recommended)
- Domain name (optional but recommended)

## Backend Deployment

### 1. Environment Setup

Create a `.env` file in the `backend` directory:

```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/emergent_mr
DB_NAME=emergent_mr
RESEND_API_KEY=re_3r6xtssc_9nn5KE3qnR9AZrGQqinZg4Wn
SENDER_EMAIL=your-verified-email@yourdomain.com
RECIPIENT_EMAIL=mukundprajapati2408@gmail.com
JWT_SECRET_KEY=your-very-strong-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-admin-password
CORS_ORIGINS=https://yourdomain.com
```

**Important:** Change all default values, especially:
- `JWT_SECRET_KEY` - Use a strong random string
- `ADMIN_PASSWORD` - Use a strong password
- `MONGO_URL` - Your production MongoDB connection string
- `SENDER_EMAIL` - Use a verified domain email from Resend
- `CORS_ORIGINS` - Your frontend domain

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Seed Database

```bash
python seed_data.py
```

### 4. Run with Gunicorn (Production)

```bash
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 5. Using Systemd (Linux)

Create `/etc/systemd/system/emergent-mr.service`:

```ini
[Unit]
Description=MR Tooling Industries API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/emergent-mr/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable emergent-mr
sudo systemctl start emergent-mr
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/emergent-mr-api`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/emergent-mr-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Frontend Deployment

### 1. Environment Setup

Create `.env.production` in `frontend` directory:

```env
REACT_APP_API_URL=https://api.yourdomain.com/api
```

### 2. Build for Production

```bash
cd frontend
npm install
npm run build
```

This creates an optimized `build` folder.

### 3. Deploy Build Folder

You have several options:

#### Option A: Nginx Static Serving

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /path/to/emergent-mr/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Option B: Netlify/Vercel

1. Connect your repository
2. Set build command: `cd frontend && npm install && npm run build`
3. Set publish directory: `frontend/build`
4. Add environment variable: `REACT_APP_API_URL=https://api.yourdomain.com/api`

#### Option C: GitHub Pages

1. Install gh-pages: `npm install --save-dev gh-pages`
2. Add to package.json:
   ```json
   "homepage": "https://yourusername.github.io/emergent-mr",
   "scripts": {
     "predeploy": "cd frontend && npm run build",
     "deploy": "gh-pages -d frontend/build"
   }
   ```
3. Deploy: `npm run deploy`

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

Certbot will automatically update your Nginx config for HTTPS.

## Post-Deployment Checklist

- [ ] All environment variables set correctly
- [ ] Database seeded with initial data
- [ ] Admin account created and password changed
- [ ] SSL certificate installed
- [ ] CORS origins configured correctly
- [ ] Email sending tested
- [ ] All API endpoints tested
- [ ] Frontend API URL configured
- [ ] Error logging set up
- [ ] Backup strategy in place

## Monitoring & Maintenance

### Logs

Backend logs:
```bash
sudo journalctl -u emergent-mr -f
```

Nginx logs:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Database

```bash
mongodump --uri="mongodb+srv://username:password@cluster.mongodb.net/emergent_mr" --out=/backup/$(date +%Y%m%d)
```

### Update Application

```bash
# Backend
cd backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart emergent-mr

# Frontend
cd frontend
git pull
npm install
npm run build
# Restart web server if needed
```

## Troubleshooting

### Backend not starting
- Check environment variables
- Check MongoDB connection
- Check port 8000 is not in use
- Check logs: `sudo journalctl -u emergent-mr`

### Frontend API errors
- Verify `REACT_APP_API_URL` is correct
- Check CORS settings in backend
- Check browser console for errors
- Verify backend is accessible

### Email not sending
- Verify Resend API key is correct
- Check sender email is verified in Resend
- Check backend logs for email errors

## Support

For issues or questions, check the logs first and ensure all environment variables are set correctly.



