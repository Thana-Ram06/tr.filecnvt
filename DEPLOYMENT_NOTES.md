# Deployment Notes

## ⚠️ Important: Vercel Limitations

This application **cannot run on Vercel** in its current form because it requires system-level dependencies that are not available in Vercel's serverless environment:

1. **LibreOffice** - Required for Office document conversions (Word, Excel, PowerPoint)
2. **Ghostscript** - Required for PDF/A conversion
3. **poppler-utils** - Required for PDF to image conversion

## Recommended Deployment Platforms

### Option 1: Render (Recommended)
- Supports system packages via buildpacks
- Free tier available
- Can install LibreOffice, Ghostscript, and poppler

### Option 2: Railway
- Supports Docker containers
- Can install system dependencies
- Easy deployment from GitHub

### Option 3: DigitalOcean App Platform
- Supports system dependencies
- Good for production deployments

### Option 4: Docker + Any VPS
- Full control over system dependencies
- Can use DigitalOcean Droplets, AWS EC2, etc.

## Docker Deployment (Recommended for Production)

See `Dockerfile` for containerized deployment.

## Local Development

This application works perfectly locally when system dependencies are installed (see README.md).
