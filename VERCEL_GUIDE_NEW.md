# Vercel Deployment Guide for Emergent MR

This project is set up as a **Monorepo** with a React Frontend and a Python (FastAPI) Backend.
The configuration allows deploying both to Vercel in a single project.

## 1. Project Structure Verification
Ensure your project looks like this (it should already be correct):
```
/
├── api/                  # Python Serverless Functions (Backend)
│   ├── index.py          # Entry point
│   ├── requirements.txt  # Python dependencies
│   └── ...
├── frontend/             # React App
│   ├── package.json
│   ├── src/
│   └── ...
├── vercel.json           # Vercel Configuration
└── ...
```

## 2. Prepare for Deployment

### A. Push to GitHub
Make sure all your code is committed and pushed to a GitHub repository.
- Ensure `api/` folder is included.
- Ensure `frontend/` folder is included.
- Ensure `vercel.json` is included.

### B. Vercel Configuration (`vercel.json`)
Your `vercel.json` is already configured to:
1. Build the frontend from the `frontend` directory.
2. Route all `/api/*` requests to the Python backend.

## 3. Deploy to Vercel

1. **Log in to Vercel** and click **"Add New..."** -> **"Project"**.
2. **Import** your GitHub repository.
3. **Configure Project**:
   - **Framework Preset**: It might detect "Create React App" or "Other". Select **Other** if possible, or let it default.
   - **Root Directory**: Leave it as `./` (Root). **DO NOT** change this to `frontend` because we need `vercel.json` in the root to control the whole deployment.

4. **Environment Variables**:
   Add the following variables in the "Environment Variables" section.
   **Crucial:** These are required for your backend to work.

   | Variable Name | Value | Description |
   |--------------|-------|-------------|
   | `MONGO_URL` | `mongodb+srv://...` | Your MongoDB Atlas connection string. |
   | `DB_NAME` | `emergent_mr` | Your database name. |
   | `JWT_SECRET_KEY` | `your-secret-key` | A long random string for security. |
   | `ADMIN_USERNAME` | `admin` | Username for admin access. |
   | `ADMIN_PASSWORD` | `your-password` | Password for admin access. |
   | `RESEND_API_KEY` | `re_...` | Your Resend API Key for emails. |
   | `SENDER_EMAIL` | `...` | Verified sender email (e.g., `onboarding@resend.dev`). |
   | `RECIPIENT_EMAIL` | `...` | Email to receive contact form submissions. |
   | `REACT_APP_API_URL` | `/api` | **IMPORTANT**: Set this to `/api` so frontend talks to backend. |
   | `CORS_ORIGINS` | `*` | Or your Vercel URL (e.g. `https://your-project.vercel.app`). |

   *Note: For `REACT_APP_API_URL`, using `/api` allows the frontend to automatically use the current domain.*

5. **Deploy**: Click **Deploy**.

## 4. Post-Deployment Verification

1. **Check Frontend**: Open the deployment URL. The site should load.
2. **Check Backend**: Go to `https://your-project.vercel.app/api`. You should see `{"message": "Hello World"}`.
3. **Check API Calls**: Try logging in or submitting a contact form.
   - If you see "Network Error" or 404, check the `REACT_APP_API_URL` variable.
   - If you see 500 Error, check `MONGO_URL` and other backend env vars.
   - You can view "Function Logs" in the Vercel Dashboard under the "Logs" tab to debug backend errors.

## Troubleshooting

- **"Module not found" in Python**:
  - Vercel installs packages from `api/requirements.txt`. Ensure all imports in `api/` files are listed there.
  
- **Frontend 404s**:
  - `vercel.json` is configured to handle client-side routing. If refreshing a page gives 404, ensure `vercel.json` rewrites are active.

- **MongoDB Connection Error**:
  - Ensure your MongoDB Atlas IP Access List allows access from anywhere (`0.0.0.0/0`) because Vercel IPs change dynamically.
