/**
 * All-in-One File Converter - Frontend JavaScript
 */

// API Base URL
const API_BASE = '/api/convert';

// Get converter type from URL
function getConverterType() {
    const path = window.location.pathname;
    const page = path.split('/').pop().replace('.html', '');
    return page;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Initialize converter page
document.addEventListener('DOMContentLoaded', function() {
    const converterType = getConverterType();
    
    if (converterType !== 'index' && converterType !== '') {
        initConverterPage(converterType);
    }
});

// Initialize converter page functionality
function initConverterPage(converterType) {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const convertBtn = document.getElementById('convertBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const messageDiv = document.getElementById('message');
    
    let selectedFile = null;

    // Map converter types to API endpoints
    const apiEndpoints = {
        'word-to-pdf': '/api/convert/word-to-pdf',
        'excel-to-pdf': '/api/convert/excel-to-pdf',
        'powerpoint-to-pdf': '/api/convert/powerpoint-to-pdf',
        'jpg-to-pdf': '/api/convert/jpg-to-pdf',
        'html-to-pdf': '/api/convert/html-to-pdf',
        'pdf-to-word': '/api/convert/pdf-to-word',
        'pdf-to-excel': '/api/convert/pdf-to-excel',
        'pdf-to-powerpoint': '/api/convert/pdf-to-powerpoint',
        'pdf-to-jpg': '/api/convert/pdf-to-jpg',
        'pdf-to-pdfa': '/api/convert/pdf-to-pdfa'
    };

    const apiEndpoint = apiEndpoints[converterType];
    if (!apiEndpoint) {
        showMessage('Invalid converter type', 'error');
        return;
    }

    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Convert button
    convertBtn.addEventListener('click', () => {
        if (selectedFile) {
            convertFile(selectedFile, apiEndpoint);
        } else {
            showMessage('Please select a file first', 'error');
        }
    });

    // Drag and drop handlers
    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    }

    // Handle file selection
    function handleFileSelect(file) {
        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.classList.add('active');
        convertBtn.disabled = false;
        hideMessage();
    }

    // Convert file
    async function convertFile(file, endpoint) {
        const formData = new FormData();
        formData.append('file', file);

        // Reset UI
        convertBtn.disabled = true;
        hideMessage();
        showProgress();

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            hideProgress();

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Conversion failed');
            }

            // Get filename from Content-Disposition header or use default
            const contentDisposition = response.headers.get('Content-Disposition');
            let downloadFilename = 'converted_file';
            
            if (contentDisposition) {
                const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
                if (matches != null && matches[1]) {
                    downloadFilename = matches[1].replace(/['"]/g, '');
                }
            }

            // Download file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = downloadFilename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showMessage('File converted successfully! Download started.', 'success');
            
            // Reset after 3 seconds
            setTimeout(() => {
                selectedFile = null;
                fileInput.value = '';
                fileInfo.classList.remove('active');
                convertBtn.disabled = false;
                hideMessage();
            }, 3000);

        } catch (error) {
            hideProgress();
            showMessage(error.message || 'An error occurred during conversion', 'error');
            convertBtn.disabled = false;
        }
    }

    // UI Helpers
    function showProgress() {
        progressContainer.classList.add('active');
        progressFill.style.width = '0%';
        progressText.textContent = 'Converting...';
        
        // Simulate progress (actual progress would come from server)
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 200);
    }

    function hideProgress() {
        progressContainer.classList.remove('active');
        progressFill.style.width = '100%';
        progressText.textContent = 'Conversion complete!';
    }

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = `message message-${type} active`;
    }

    function hideMessage() {
        messageDiv.classList.remove('active');
    }
}

