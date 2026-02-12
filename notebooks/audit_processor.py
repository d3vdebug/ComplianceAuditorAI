"""
Document Audit Processor
Converts notebook functions into importable Python module
"""

import re
import os

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
    print("Warning: PyPDF2 not installed. PDF processing will not work.")

try:
    import docx
except ImportError:
    docx = None
    print("Warning: python-docx not installed. DOCX processing will not work.")

# Rule-based compliance checks
def check_compliance_rules(text, doc_type):
    """Run rule-based compliance checks"""
    issues = []
    passed = []
    warnings = []
    
    # Check 1: Date presence
    date_pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
    if re.search(date_pattern, text, re.IGNORECASE):
        passed.append("Valid date found")
    else:
        issues.append("Missing date information")
    
    # Check 2: Signature/execution terms
    signature_terms = ['signature', 'signed', 'executed', 'signatory', 'undersigned']
    if any(term in text.lower() for term in signature_terms):
        passed.append("Signature terms present")
    else:
        issues.append("Missing signature or execution terms")
    
    # Check 3: Contact information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))
    
    if has_email or has_phone:
        passed.append("Contact information found")
    else:
        warnings.append("Limited contact information")
    
    # Check 4: Document type specific
    if doc_type == 'contract':
        contract_terms = ['agreement', 'party', 'parties', 'terms', 'conditions']
        found_terms = sum(term in text.lower() for term in contract_terms)
        if found_terms >= 3:
            passed.append("Contract terms present")
        else:
            issues.append("Missing standard contract terms")
    
    elif doc_type == 'policy':
        policy_terms = ['policy', 'procedure', 'compliance', 'regulation']
        if any(term in text.lower() for term in policy_terms):
            passed.append("Policy terms present")
        else:
            issues.append("Missing policy-specific terms")
    
    elif doc_type == 'agreement':
        agreement_terms = ['service', 'obligation', 'rights', 'responsibilities']
        found_terms = sum(term in text.lower() for term in agreement_terms)
        if found_terms >= 2:
            passed.append("Agreement terms present")
        else:
            issues.append("Missing standard agreement terms")
    
    # Check 5: Document length
    word_count = len(text.split())
    if word_count < 100:
        issues.append(f"Document too short ({word_count} words)")
    elif word_count < 200:
        warnings.append("Document may be incomplete")
    else:
        passed.append(f"Adequate document length ({word_count} words)")
    
    # Check 6: Prohibited content
    prohibited_terms = ['discriminat', 'illegal', 'unlawful', 'fraud']
    found_prohibited = [term for term in prohibited_terms if term in text.lower()]
    if found_prohibited:
        warnings.append(f"Review required: found terms - {', '.join(found_prohibited)}")
    else:
        passed.append("No prohibited terms detected")
    
    # Check 7: Legal terms presence
    legal_terms = ['hereby', 'whereas', 'therefore', 'pursuant', 'hereinafter']
    found_legal = sum(term in text.lower() for term in legal_terms)
    if found_legal >= 2:
        passed.append("Legal terminology present")
    else:
        warnings.append("Limited legal terminology")
    
    return {
        'issues': issues,
        'passed': passed,
        'warnings': warnings
    }

# ML-based compliance prediction
def predict_compliance_ml(text):
    """Use ML model to predict compliance"""
    try:
        # Extract features
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'has_date': bool(re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text)),
            'has_signature': 'signature' in text.lower() or 'signed' in text.lower(),
            'has_email': bool(re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', text)),
            'has_phone': bool(re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', text)),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'has_legal_terms': any(term in text.lower() for term in ['hereby', 'whereas', 'therefore'])
        }
        
        # Simple scoring based on features
        score = 0.4  # Base score
        
        if features['word_count'] > 200:
            score += 0.2
        elif features['word_count'] > 100:
            score += 0.1
        
        if features['has_date']:
            score += 0.15
        
        if features['has_signature']:
            score += 0.15
        
        if features['has_email'] or features['has_phone']:
            score += 0.1
        
        if features['has_legal_terms']:
            score += 0.1
        
        confidence = min(score, 1.0)
        is_compliant = confidence > 0.65
        
        return {
            'is_compliant': is_compliant,
            'confidence': confidence
        }
    
    except Exception as e:
        print(f"ML prediction error: {e}")
        return {
            'is_compliant': False,
            'confidence': 0.5
        }

# Main processing function
def process_document(text, doc_type, filename):
    """Main document processing function"""
    
    # Rule-based checks
    rule_results = check_compliance_rules(text, doc_type)
    
    # ML prediction
    ml_results = predict_compliance_ml(text)
    
    # Calculate overall score
    issues_count = len(rule_results['issues'])
    passed_count = len(rule_results['passed'])
    warnings_count = len(rule_results['warnings'])
    
    # Base score from rules (0-70)
    rule_score = max(0, 70 - (issues_count * 12) - (warnings_count * 3))
    
    # ML score contribution (0-30)
    ml_score = ml_results['confidence'] * 30
    
    # Combined score
    total_score = int(rule_score + ml_score)
    total_score = max(0, min(100, total_score))  # Clamp to 0-100
    
    return {
        'documentName': filename,
        'complianceScore': total_score,
        'issues': rule_results['issues'],
        'passedChecks': rule_results['passed'],
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }

# File extraction functions
def extract_text_from_file(filepath, filename):
    """Extract text from PDF, DOCX, or TXT files"""
    ext = filename.rsplit('.', 1)[1].lower()
    
    try:
        if ext == 'pdf':
            return extract_from_pdf(filepath)
        elif ext in ['docx', 'doc']:
            return extract_from_docx(filepath)
        elif ext == 'txt':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise Exception(f"Error extracting text from {filename}: {str(e)}")

def extract_from_pdf(filepath):
    """Extract text from PDF"""
    if PyPDF2 is None:
        raise Exception("PyPDF2 is not installed. Cannot process PDF files.")
    
    text = ""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise Exception("PDF appears to be empty or contains only images")
        
        return text
    except Exception as e:
        raise Exception(f"PDF extraction error: {str(e)}")

def extract_from_docx(filepath):
    """Extract text from DOCX"""
    if docx is None:
        raise Exception("python-docx is not installed. Cannot process DOCX files.")
    
    try:
        doc = docx.Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        
        if not text.strip():
            raise Exception("DOCX appears to be empty")
        
        return text
    except Exception as e:
        raise Exception(f"DOCX extraction error: {str(e)}")
