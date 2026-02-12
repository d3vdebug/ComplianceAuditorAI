# Quick Start Guide

## Running the Complete Application

### Option 1: Using Start Scripts (Windows)

**Backend (Terminal 1):**
```bash
cd backend
start.bat
```

**Frontend (Terminal 2):**
```bash
cd frontend
start.bat
```

### Option 2: Manual Commands

**Backend (Terminal 1):**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm install
npm start
```

## What You Should See

**Backend Terminal:**
```
============================================================
🚀 Document Compliance Audit API
============================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/api/health
Upload endpoint: http://localhost:5000/api/audit
============================================================
```

**Frontend Browser:**
- Opens automatically at http://localhost:3000
- Shows Document Compliance Audit interface
- Drag-and-drop file upload area

## Testing

1. Open http://localhost:3000
2. Drag and drop a PDF, DOCX, or TXT file
3. Select document type
4. Click "Run Compliance Audit"
5. View results with score and detailed analysis

## Sample Test Files

Create a simple test file:

**test_contract.txt:**
```
EMPLOYMENT CONTRACT

Date: January 15, 2024
Employee: John Smith
Position: Software Engineer

TERMS AND CONDITIONS:
This agreement outlines the terms of employment between the parties.

Salary: $85,000 per annum
Benefits: Health insurance, 401k
Start Date: February 1, 2024

By signing below, both parties agree to the terms.

Signature: [Signed]
Employee: John Smith
Employer: ABC Corporation

Contact: hr@company.com
Phone: 555-123-4567
```

Save this as `test_contract.txt` and upload it to test the system.

## Expected Result

```json
{
  "documentName": "test_contract.txt",
  "complianceScore": 85-95,
  "issues": [],
  "passedChecks": [
    "Valid date found",
    "Signature terms present",
    "Contact information found",
    "Contract terms present",
    "Adequate document length",
    "No prohibited terms detected",
    "Legal terminology present"
  ],
  "timestamp": "2026-02-12T..."
}
```

## Troubleshooting

**Problem:** Backend won't start
- **Solution:** Ensure Python 3.8+ is installed
- Check that you're in the `backend` directory
- Run `pip install -r requirements.txt` manually

**Problem:** Frontend shows connection error
- **Solution:** Make sure backend is running on port 5000
- Check backend terminal for errors

**Problem:** File upload fails
- **Solution:** Ensure file is under 16MB
- Use text-based PDFs (not scanned images)
- Check file format is PDF, DOCX, DOC, or TXT

## System Requirements

- **Python:** 3.8 or higher
- **Node.js:** 14 or higher
- **RAM:** 2GB minimum
- **Disk Space:** 500MB for dependencies

## Port Information

- **Backend API:** http://localhost:5000
- **Frontend UI:** http://localhost:3000

If these ports are in use, you can change them in:
- Backend: `backend/app.py` (line 117)
- Frontend: `frontend/src/components/AuditForm.tsx` (line 13)

## Next Steps

Once running successfully:
1. Test with various document types
2. Try different document formats (PDF, DOCX, TXT)
3. Experiment with incomplete documents to see lower scores
4. Check the Jupyter notebooks for data exploration
