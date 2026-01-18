# All-in-One File Converter

A professional, production-ready file conversion web application similar to iLovePDF, built with Flask and modern web technologies.

## Features

### Supported Conversions

**To PDF:**
- 📝 WORD → PDF (.doc, .docx)
- 📊 EXCEL → PDF (.xls, .xlsx)
- 📑 POWERPOINT → PDF (.ppt, .pptx)
- 🖼️ JPG → PDF (.jpg, .jpeg, .png)
- 🌐 HTML → PDF (.html, .htm)

**From PDF:**
- 📄 PDF → WORD (.docx)
- 📄 PDF → EXCEL (.xlsx)
- 📄 PDF → POWERPOINT (.pptx)
- 📄 PDF → JPG (multi-page support with ZIP)
- 📄 PDF → PDF/A (archival format)

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Conversion Engines**:
  - LibreOffice (headless) - Office document conversions
  - pdf2image + Pillow - PDF to image conversions
  - pdf2docx - PDF to Word conversion
  - pdf2pptx - PDF to PowerPoint conversion
  - Ghostscript - PDF/A conversion

## Prerequisites

### System Requirements

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **LibreOffice** (for Office document conversions)
   - **Windows**: Download from [LibreOffice.org](https://www.libreoffice.org/download/)
   - **Linux**: 
     ```bash
     sudo apt-get update
     sudo apt-get install libreoffice
     ```
   - **macOS**: 
     ```bash
     brew install --cask libreoffice
     ```

3. **Ghostscript** (for PDF/A conversion)
   - **Windows**: Download from [Ghostscript.com](https://www.ghostscript.com/download/gsdnld.html)
   - **Linux**: 
     ```bash
     sudo apt-get install ghostscript
     ```
   - **macOS**: 
     ```bash
     brew install ghostscript
     ```

4. **poppler-utils** (required for pdf2image)
   - **Windows**: Download from [poppler-utils](http://blog.alivate.com.au/poppler-windows/) - Add `bin` folder to PATH
   - **Linux**: 
     ```bash
     sudo apt-get install poppler-utils
     ```
   - **macOS**: 
     ```bash
     brew install poppler
     ```

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd trconverter
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify System Tools

Make sure these commands work in your terminal:

```bash
# Check LibreOffice
soffice --version

# Check Ghostscript (Windows: gswin64c, Linux/macOS: gs)
gswin64c --version  # Windows
# OR
gs --version  # Linux/macOS

# Check poppler (Windows: pdftoppm, Linux/macOS: pdftoppm)
pdftoppm -v
```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Project Structure

```
trconverter/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Homepage
│   └── converter.html    # Converter page template
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Stylesheets
│   └── js/
│       └── app.js        # Frontend JavaScript
├── uploads/              # Temporary upload directory (auto-created)
└── outputs/              # Converted files directory (auto-created)
```

## Usage

1. **Access the Homepage**: Open `http://localhost:5000` in your browser
2. **Select Converter**: Click on any converter card from the homepage
3. **Upload File**: 
   - Click the upload area to browse files
   - OR drag and drop a file onto the upload area
4. **Convert**: Click the "Convert File" button
5. **Download**: The converted file will automatically download when ready

## API Endpoints

All converters use REST API endpoints:

- `POST /api/convert/word-to-pdf`
- `POST /api/convert/excel-to-pdf`
- `POST /api/convert/powerpoint-to-pdf`
- `POST /api/convert/jpg-to-pdf`
- `POST /api/convert/html-to-pdf`
- `POST /api/convert/pdf-to-word`
- `POST /api/convert/pdf-to-excel`
- `POST /api/convert/pdf-to-powerpoint`
- `POST /api/convert/pdf-to-jpg`
- `POST /api/convert/pdf-to-pdfa`
- `GET /api/health` - Health check endpoint

## Features & Best Practices

✅ **High Quality Output** - All conversions maintain high quality  
✅ **Automatic Cleanup** - Temporary files are automatically deleted  
✅ **Error Handling** - Comprehensive error messages for troubleshooting  
✅ **Drag & Drop** - Modern file upload experience  
✅ **Progress Indicators** - Visual feedback during conversion  
✅ **Responsive Design** - Works on desktop and mobile devices  
✅ **Security** - File validation and secure filename handling  

## Troubleshooting

### LibreOffice Not Found
- Ensure LibreOffice is installed and `soffice` command is in your PATH
- Windows: Add LibreOffice installation path to system PATH
- Verify with: `soffice --version`

### Ghostscript Not Found
- Windows: Use `gswin64c` (64-bit) or `gswin32c` (32-bit)
- Update `app.py` line 551 if using 32-bit Ghostscript
- Verify with: `gswin64c --version` (Windows) or `gs --version` (Linux/macOS)

### pdf2image Errors
- Ensure poppler-utils is installed and accessible
- Check PATH includes poppler binaries
- Verify with: `pdftoppm -v`

### Conversion Timeout
- Large files may take longer - adjust timeout in `app.py` if needed
- Default timeout is 60 seconds per conversion

### Permission Errors
- Ensure `uploads/` and `outputs/` directories are writable
- These directories are auto-created on first run

## Development Notes

- The application uses Flask's debug mode by default (see `app.py` line 592)
- For production, set `debug=False` and use a proper WSGI server
- All file paths use `secure_filename()` to prevent directory traversal
- CORS is enabled for API endpoints

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check:
1. All system dependencies are installed correctly
2. Required tools are in your system PATH
3. Virtual environment is activated
4. All Python packages are installed

---

**Built with ❤️ using Flask, LibreOffice, and modern web technologies**
