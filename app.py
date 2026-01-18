"""
All-in-One File Converter Backend
Flask REST API for file conversions
"""

import os
import subprocess
import shutil
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import pdf2docx
from pdf2pptx import convert_pdf2pptx
import logging
import zipfile

app = Flask(__name__)
CORS(app)

# Configure directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt',
    'jpg', 'jpeg', 'png', 'pdf', 'html', 'htm'
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_files(*filepaths):
    """Clean up temporary files"""
    for filepath in filepaths:
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not delete {filepath}: {e}")

# ==================== WORD → PDF ====================
@app.route('/api/convert/word-to-pdf', methods=['POST'])
def word_to_pdf():
    """Convert Word document to PDF using LibreOffice"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith(('.doc', '.docx')):
            return jsonify({'error': 'Invalid file type. Please upload .doc or .docx'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        # Convert using LibreOffice
        output_dir = os.path.join(OUTPUT_FOLDER, f"word_pdf_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        # Find output PDF
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        if not os.path.exists(output_path):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        # Move to outputs with unique name
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pdf")
        shutil.move(output_path, final_output)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pdf")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"Word to PDF error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== EXCEL → PDF ====================
@app.route('/api/convert/excel-to-pdf', methods=['POST'])
def excel_to_pdf():
    """Convert Excel document to PDF using LibreOffice"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith(('.xls', '.xlsx')):
            return jsonify({'error': 'Invalid file type. Please upload .xls or .xlsx'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        output_dir = os.path.join(OUTPUT_FOLDER, f"excel_pdf_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        if not os.path.exists(output_path):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pdf")
        shutil.move(output_path, final_output)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pdf")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"Excel to PDF error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== POWERPOINT → PDF ====================
@app.route('/api/convert/powerpoint-to-pdf', methods=['POST'])
def powerpoint_to_pdf():
    """Convert PowerPoint presentation to PDF using LibreOffice"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith(('.ppt', '.pptx')):
            return jsonify({'error': 'Invalid file type. Please upload .ppt or .pptx'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        output_dir = os.path.join(OUTPUT_FOLDER, f"pptx_pdf_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        if not os.path.exists(output_path):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pdf")
        shutil.move(output_path, final_output)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pdf")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PowerPoint to PDF error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== JPG → PDF ====================
@app.route('/api/convert/jpg-to-pdf', methods=['POST'])
def jpg_to_pdf():
    """Convert JPG/PNG image to PDF using PIL"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                return jsonify({'error': 'Invalid file type. Please upload .jpg, .jpeg, or .png'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        # Convert image to PDF
        image = Image.open(input_path)
        rgb_image = image.convert('RGB')
        
        base_name = os.path.splitext(filename)[0]
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pdf")
        rgb_image.save(final_output, 'PDF', resolution=100.0)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pdf")
    
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"JPG to PDF error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== HTML → PDF ====================
@app.route('/api/convert/html-to-pdf', methods=['POST'])
def html_to_pdf():
    """Convert HTML file to PDF using LibreOffice"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith(('.html', '.htm')):
            return jsonify({'error': 'Invalid file type. Please upload .html or .htm'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        output_dir = os.path.join(OUTPUT_FOLDER, f"html_pdf_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        if not os.path.exists(output_path):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pdf")
        shutil.move(output_path, final_output)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pdf")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"HTML to PDF error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== PDF → WORD ====================
@app.route('/api/convert/pdf-to-word', methods=['POST'])
def pdf_to_word():
    """Convert PDF to Word document using pdf2docx"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload .pdf'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        base_name = os.path.splitext(filename)[0]
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.docx")
        
        # Convert PDF to DOCX
        cv = pdf2docx.Converter(input_path)
        cv.convert(final_output)
        cv.close()
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.docx")
    
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PDF to Word error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== PDF → EXCEL ====================
@app.route('/api/convert/pdf-to-excel', methods=['POST'])
def pdf_to_excel():
    """Convert PDF to Excel using LibreOffice (works for PDFs with tables)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload .pdf'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        output_dir = os.path.join(OUTPUT_FOLDER, f"pdf_excel_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        # LibreOffice can convert PDF to various formats including Calc (Excel)
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'xlsx',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.xlsx")
        
        if not os.path.exists(output_path):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.xlsx")
        shutil.move(output_path, final_output)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.xlsx")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PDF to Excel error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== PDF → POWERPOINT ====================
@app.route('/api/convert/pdf-to-powerpoint', methods=['POST'])
def pdf_to_powerpoint():
    """Convert PDF to PowerPoint using pdf2pptx"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload .pdf'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        base_name = os.path.splitext(filename)[0]
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.pptx")
        
        # Convert PDF to PPTX
        convert_pdf2pptx(input_path, final_output)
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}.pptx")
    
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PDF to PowerPoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== PDF → JPG ====================
@app.route('/api/convert/pdf-to-jpg', methods=['POST'])
def pdf_to_jpg():
    """Convert PDF to JPG images using pdf2image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload .pdf'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        # Convert PDF pages to images
        images = convert_from_path(input_path, dpi=300)
        
        if not images:
            cleanup_files(input_path)
            return jsonify({'error': 'No pages found in PDF'}), 500
        
        # If single page, return single JPG; if multiple pages, create ZIP
        base_name = os.path.splitext(filename)[0]
        
        if len(images) == 1:
            # Single page - return JPG
            final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.jpg")
            images[0].save(final_output, 'JPEG', quality=95)
            cleanup_files(input_path)
            return send_file(final_output, as_attachment=True, download_name=f"{base_name}.jpg")
        else:
            # Multiple pages - create ZIP
            zip_path = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for i, img in enumerate(images, 1):
                    img_path = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}_page_{i}.jpg")
                    img.save(img_path, 'JPEG', quality=95)
                    zipf.write(img_path, f"{base_name}_page_{i}.jpg")
                    os.remove(img_path)
            
            cleanup_files(input_path)
            return send_file(zip_path, as_attachment=True, download_name=f"{base_name}.zip")
    
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PDF to JPG error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== PDF → PDF/A ====================
@app.route('/api/convert/pdf-to-pdfa', methods=['POST'])
def pdf_to_pdfa():
    """Convert PDF to PDF/A format using Ghostscript"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename) or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload .pdf'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
        file.save(input_path)
        
        base_name = os.path.splitext(filename)[0]
        final_output = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{base_name}_pdfa.pdf")
        
        # Convert to PDF/A-1b using Ghostscript
        cmd = [
            'gswin64c' if os.name == 'nt' else 'gs',
            '-dPDFA=1',
            '-dBATCH',
            '-dNOPAUSE',
            '-dUseCIEColor',
            '-sProcessColorModel=DeviceRGB',
            '-sDEVICE=pdfwrite',
            '-sPDFACompatibilityPolicy=1',
            f'-sOutputFile={final_output}',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            cleanup_files(input_path)
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        if not os.path.exists(final_output):
            cleanup_files(input_path)
            return jsonify({'error': 'Conversion failed: Output file not found'}), 500
        
        cleanup_files(input_path)
        
        return send_file(final_output, as_attachment=True, download_name=f"{base_name}_pdfa.pdf")
    
    except subprocess.TimeoutExpired:
        cleanup_files(input_path)
        return jsonify({'error': 'Conversion timeout'}), 500
    except Exception as e:
        cleanup_files(input_path)
        logger.error(f"PDF to PDF/A error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== FRONTEND ROUTES ====================
@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

# Converter pages
@app.route('/<converter_type>.html')
def converter_page(converter_type):
    """Serve converter pages"""
    converter_configs = {
        'word-to-pdf': {
            'title': 'WORD → PDF Converter',
            'description': 'Convert Word documents to PDF format',
            'supported_formats': '.doc, .docx',
            'accept_types': '.doc,.docx'
        },
        'excel-to-pdf': {
            'title': 'EXCEL → PDF Converter',
            'description': 'Convert Excel spreadsheets to PDF format',
            'supported_formats': '.xls, .xlsx',
            'accept_types': '.xls,.xlsx'
        },
        'powerpoint-to-pdf': {
            'title': 'POWERPOINT → PDF Converter',
            'description': 'Convert PowerPoint presentations to PDF format',
            'supported_formats': '.ppt, .pptx',
            'accept_types': '.ppt,.pptx'
        },
        'jpg-to-pdf': {
            'title': 'JPG → PDF Converter',
            'description': 'Convert JPG/PNG images to PDF documents',
            'supported_formats': '.jpg, .jpeg, .png',
            'accept_types': '.jpg,.jpeg,.png'
        },
        'html-to-pdf': {
            'title': 'HTML → PDF Converter',
            'description': 'Convert HTML files to PDF documents',
            'supported_formats': '.html, .htm',
            'accept_types': '.html,.htm'
        },
        'pdf-to-word': {
            'title': 'PDF → WORD Converter',
            'description': 'Convert PDF documents to Word format',
            'supported_formats': '.pdf',
            'accept_types': '.pdf'
        },
        'pdf-to-excel': {
            'title': 'PDF → EXCEL Converter',
            'description': 'Convert PDF documents to Excel format',
            'supported_formats': '.pdf',
            'accept_types': '.pdf'
        },
        'pdf-to-powerpoint': {
            'title': 'PDF → POWERPOINT Converter',
            'description': 'Convert PDF documents to PowerPoint format',
            'supported_formats': '.pdf',
            'accept_types': '.pdf'
        },
        'pdf-to-jpg': {
            'title': 'PDF → JPG Converter',
            'description': 'Convert PDF pages to JPG images',
            'supported_formats': '.pdf',
            'accept_types': '.pdf'
        },
        'pdf-to-pdfa': {
            'title': 'PDF → PDF/A Converter',
            'description': 'Convert PDF to PDF/A archive format',
            'supported_formats': '.pdf',
            'accept_types': '.pdf'
        }
    }
    
    config = converter_configs.get(converter_type)
    if config:
        return render_template('converter.html', **config)
    else:
        return render_template('index.html')

# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'File Converter API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

