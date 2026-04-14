# Roommate Dekho - Vercel Deployment Guide

## Quick Deploy to Vercel

### Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Have a Vercel account (sign up at vercel.com)
3. MongoDB Atlas account with connection string

### Deployment Steps

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy the Application**
   ```bash
   vercel --prod
   ```

3. **Configure Environment Variables** (in Vercel Dashboard)
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add the following:
     - `MONGODB_URI`: Your MongoDB connection string
     - `GOOGLE_MAPS_API_KEY`: Your Google Maps API key

### Alternative: Deploy via GitHub

1. Push your code to GitHub
2. Import repository in Vercel dashboard
3. Vercel will auto-detect Flask and configure
4. Add environment variables in project settings
5. Deploy!

### Post-Deployment

- Your app will be live at: `your-project-name.vercel.app`
- Configure custom domain in Vercel settings (optional)
- Monitor logs in Vercel dashboard

### Important Notes

- Static files are served from `/static` directory
- MongoDB Atlas must allow connections from all IPs (0.0.0.0/0) for Vercel
- Google Maps API key should have proper restrictions
- All routes are handled by `application.py`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python application.py

# Access at http://localhost:5000
```

## Troubleshooting

**MongoDB Connection Fails:**
- Check MongoDB Atlas network access settings
- Verify connection string in environment variables

**Static Files Not Loading:**
- Ensure `static/` folder structure is correct
- Check Vercel logs for 404 errors

**Google Maps Not Working:**
- Verify API key is set correctly
- Check API restrictions and billing

For more help, visit: https://vercel.com/docs
