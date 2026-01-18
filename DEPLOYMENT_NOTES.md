# Deployment Notes

## ⚠️ Important: Vercel is NOT Compatible

This application **CANNOT run on Vercel** due to two critical issues:

1. **Size Limit Exceeded** - Python packages (pdf2image, Pillow, pdf2docx) exceed Vercel's 250 MB serverless function limit
2. **System Dependencies Missing** - Vercel cannot install:
   - **LibreOffice** - Required for Office document conversions (Word, Excel, PowerPoint)
   - **Ghostscript** - Required for PDF/A conversion
   - **poppler-utils** - Required for PDF to image conversion

## Recommended Deployment Platforms

### Option 1: Render (Easiest - Recommended)
**Use the included `render.yaml` for quick deployment:**

1. Go to https://render.com and sign up
2. Connect your GitHub repository: `Thana-Ram06/tr.filecnvt`
3. Click "New +" → "Blueprint"
4. Render will auto-detect `render.yaml` and deploy
5. Your app will be live with all system dependencies!

**Or manually:**
- Select "Web Service"
- Use Docker deployment (uses the included `Dockerfile`)
- Free tier available

### Option 2: Railway
1. Go to https://railway.app
2. Connect GitHub repository
3. Select "Deploy from Dockerfile"
4. Railway will build and deploy automatically

### Option 3: DigitalOcean App Platform
- Supports Docker deployments
- Use the included `Dockerfile`
- Good for production deployments

### Option 4: Any VPS with Docker
- DigitalOcean Droplets
- AWS EC2
- Google Cloud Compute Engine
- Azure Virtual Machines

Run:
```bash
docker build -t file-converter .
docker run -p 5000:5000 file-converter
```

## Docker Deployment

The `Dockerfile` is included and ready to use. It automatically:
- Installs Python 3.11
- Installs LibreOffice, Ghostscript, and poppler-utils
- Installs all Python dependencies
- Runs the Flask app on port 5000

## Local Development

This application works perfectly locally when system dependencies are installed (see README.md).
