# Backend API

Flask-based REST API for document compliance auditing.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The API will start on `http://localhost:5000`

## Endpoints

### POST /api/audit
Upload a document for compliance analysis.

**Parameters:**
- `file`: Document file (PDF, DOCX, DOC, TXT) - required
- `docType`: Document type (contract, agreement, policy, other) - optional

**Response:**
```json
{
  "documentName": "contract.pdf",
  "complianceScore": 85,
  "issues": ["Missing signature terms"],
  "passedChecks": ["Valid date found", "Contact information present"],
  "timestamp": "2026-02-12T10:30:00"
}
```

### GET /api/health
Check API health status.

### GET /api/stats
Get API statistics.

## File Requirements

- Supported formats: PDF, DOC, DOCX, TXT
- Max file size: 16MB
- Text encoding: UTF-8
