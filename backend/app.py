from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import json
from datetime import datetime

# Import processing functions from notebooks
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'notebooks'))
from audit_processor import process_document, extract_text_from_file

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/audit', methods=['POST'])
def audit_document():
    """Main endpoint for document audit"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PDF, DOCX, DOC, or TXT'}), 400
        
        # Get document type from form data
        doc_type = request.form.get('docType', 'contract')
        
        # Save file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Extract text from file
            document_text = extract_text_from_file(filepath, filename)
            
            if not document_text or len(document_text.strip()) < 50:
                return jsonify({
                    'error': 'Could not extract sufficient text from document. Please check if the file is readable.'
                }), 400
            
            # Process document through audit workflow
            audit_results = process_document(document_text, doc_type, filename)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(audit_results), 200
            
        except Exception as e:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return jsonify({
            'error': f'Error processing document: {str(e)}'
        }), 500

@app.route('/api/batch-audit', methods=['POST'])
def batch_audit():
    """Endpoint for batch document processing"""
    try:
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                try:
                    document_text = extract_text_from_file(filepath, filename)
                    doc_type = request.form.get('docType', 'contract')
                    audit_result = process_document(document_text, doc_type, filename)
                    audit_result['filename'] = filename
                    results.append(audit_result)
                    os.remove(filepath)
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'error': str(e),
                        'score': 0
                    })
                    if os.path.exists(filepath):
                        os.remove(filepath)
        
        return jsonify({'results': results}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    return jsonify({
        'total_audits': 0,
        'average_score': 0,
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': MAX_FILE_SIZE / (1024 * 1024)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Document Compliance Audit API")
    print("=" * 60)
    print(f"Server running on: http://localhost:5000")
    print(f"Health check: http://localhost:5000/api/health")
    print(f"Upload endpoint: http://localhost:5000/api/audit")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
