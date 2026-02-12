# Compliance Auditor AI

An AI/ML-powered application for running document compliance audits with a React frontend, Flask backend API, and Jupyter notebook data processing.

## 🏗️ Project Structure

```
Microsoft Elevate Internship Project/
├── frontend/                    # React TypeScript application
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── AuditForm.tsx   # Document upload form
│   │   │   ├── Header.tsx      # Application header
│   │   │   └── Results.tsx     # Audit results display
│   │   ├── App.tsx             # Main application component
│   │   ├── App.css             # Application styles
│   │   ├── index.tsx           # Application entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # Node dependencies
│   └── tsconfig.json           # TypeScript configuration
│
├── backend/                     # Flask API server
│   ├── app.py                  # Main Flask application
│   ├── requirements.txt        # Python API dependencies
│   ├── README.md               # API documentation
│   └── uploads/                # Temporary file storage (auto-created)
│
└── notebooks/                   # Jupyter notebooks & processing
    ├── doc_audit_workflow.ipynb    # Main audit workflow
    ├── preprocessing.ipynb          # Data preprocessing
    ├── audit_processor.py          # Processing module for API
    └── requirements.txt             # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v14 or higher) and npm
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

### Installation & Running

#### 1. Backend Setup (Flask API)

Open a terminal and run:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Expected output:**
```
============================================================
🚀 Document Compliance Audit API
============================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/api/health
Upload endpoint: http://localhost:5000/api/audit
============================================================
```

The backend API will run on **http://localhost:5000**

⚠️ **Keep this terminal running!**

---

#### 2. Frontend Setup (React)

Open a **new terminal** and run:

```bash
cd frontend
npm install
npm start
```

The React app will automatically open at **http://localhost:3000**

⚠️ **Keep this terminal running too!**

---

#### 3. Notebook Setup (Optional - for development)

```bash
cd notebooks
pip install -r requirements.txt
jupyter notebook
```

Open the notebooks in your browser:
- `preprocessing.ipynb` - Data preprocessing pipeline
- `doc_audit_workflow.ipynb` - Complete audit workflow

## 📋 How to Use

1. **Open the app** at http://localhost:3000 in your browser
2. **Drag and drop** a document (PDF, DOC, DOCX, or TXT) onto the upload area
3. **Select document type** (Contract, Agreement, Policy, or Other)
4. **Click "Run Compliance Audit"**
5. **View results** showing:
   - Compliance score (0-100)
   - Issues found
   - Passed checks
   - Warnings

## ✨ Features

### Frontend (React + TypeScript)
- ✅ Drag and drop file upload interface
- ✅ Real-time processing with loading states
- ✅ Beautiful gradient UI with animations
- ✅ Comprehensive results dashboard
- ✅ Responsive design (desktop & mobile)
- ✅ Error handling with user-friendly messages

### Backend API (Flask)
- ✅ RESTful API endpoints
- ✅ Multi-format document processing (PDF, DOCX, DOC, TXT)
- ✅ Secure file upload and validation
- ✅ Automatic file cleanup after processing
- ✅ CORS enabled for frontend access
- ✅ Health check and statistics endpoints

### Processing Engine (Python + ML)
- ✅ Text extraction from multiple formats
- ✅ Rule-based compliance checks
- ✅ ML-powered scoring system
- ✅ Feature engineering and analysis
- ✅ Comprehensive audit reporting

## 🛠️ Technology Stack

**Frontend:**
- React 17
- TypeScript
- CSS3 with gradients & animations

**Backend:**
- Flask 3.0 (Python web framework)
- Flask-CORS for cross-origin requests
- PyPDF2 for PDF processing
- python-docx for Word documents

**Processing:**
- scikit-learn for ML
- pandas & numpy for data processing
- Regular expressions for pattern matching

## 🔍 Compliance Checks

The system automatically checks for:

1. **✓ Date Information** - Validates presence of dates
2. **✓ Signature Terms** - Checks for signature/execution language
3. **✓ Contact Information** - Verifies email/phone presence
4. **✓ Document-Specific Terms** - Contract, policy, or agreement terminology
5. **✓ Document Completeness** - Validates minimum word count
6. **✓ Prohibited Content** - Scans for flagged terms
7. **✓ Legal Terminology** - Checks for formal legal language

## 📊 Scoring System

**Total Score: 0-100**

- **Rule-based score:** 0-70 points
  - Critical issues: -12 points each
  - Warnings: -3 points each
  
- **ML confidence score:** 0-30 points
  - Based on document features and structure

**Score Interpretation:**
- **90-100:** Excellent compliance ✅
- **75-89:** Good compliance 👍
- **60-74:** Acceptable compliance ⚠️
- **Below 60:** Needs review ❌

## 🧪 Testing the API

### Test with cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Upload a document
curl -X POST http://localhost:5000/api/audit \
  -F "file=@your_document.pdf" \
  -F "docType=contract"
```

### Sample Documents

Test with:
- Employment contracts (PDF/DOCX)
- Service agreements (PDF/DOCX)
- Privacy policies (PDF/TXT)

Find free samples at:
- **Template.net** - https://www.template.net/
- **file-examples.com** - https://file-examples.com/
- **PandaDoc** - https://www.pandadoc.com/templates/

## 🐛 Troubleshooting

### Backend won't start
Make sure you're in the `backend` folder with dependencies installed:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend shows "Error processing document"
Ensure backend is running on http://localhost:5000

### PDF text extraction fails
Use text-based PDFs (not scanned images)

## 📂 File Requirements

**Supported:** PDF, DOCX, DOC, TXT  
**Max size:** 16 MB  
**Encoding:** UTF-8 for text files

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/audit` | Single document audit |
| POST | `/api/batch-audit` | Multiple documents |
| GET | `/api/stats` | API statistics |

## 📝 Development

**Frontend:**
```bash
cd frontend
npm start       # Start dev server
npm build       # Build for production
npm test        # Run tests
```

**Backend:**
```bash
cd backend
python app.py   # Start Flask server
```

**Notebooks:**
```bash
cd notebooks
jupyter notebook
```

## 🔄 Future Enhancements

- [ ] User authentication
- [ ] Database for audit history
- [ ] Advanced ML models (BERT, GPT)
- [ ] PDF report generation
- [ ] Batch processing queue
- [ ] Docker containerization

## 📄 License

Educational project - Microsoft Elevate Internship Program

### Quick Start

**Terminal 1 - Backend:**
```bash
cd backend && pip install -r requirements.txt && python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend && npm install && npm start
```

Visit **http://localhost:3000** and upload a document! 🎉
