import React, { useState, useRef } from 'react';
import './AuditForm.css';

interface AuditFormProps {
  onAuditComplete: (results: any) => void;
}

const AuditForm: React.FC<AuditFormProps> = ({ onAuditComplete }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [docType, setDocType] = useState<string>('contract');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_URL = 'http://localhost:5000/api';

  const validateAndSetFile = (file: File) => {
    setError('');
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'text/plain'];
    const maxSize = 16 * 1024 * 1024; // 16MB

    if (!validTypes.includes(file.type)) {
      setError('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files.');
      return;
    }

    if (file.size > maxSize) {
      setError('File size exceeds 16MB limit.');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('docType', docType);

    try {
      const response = await fetch(`${API_URL}/audit`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to process document');
      }

      onAuditComplete(data);

      // Reset form
      setSelectedFile(null);
      setDocType('contract');

    } catch (err: any) {
      setError(err.message || 'Error processing document. Please ensure the backend server is running on http://localhost:5000');
      console.error('Audit error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="audit-form-container">
      <form onSubmit={handleSubmit} className="audit-form">
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="doc-type">Document Type:</label>
          <select
            id="doc-type"
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            className="doc-type-select"
            disabled={isLoading}
          >
            <option value="contract">📄 Employment Contract</option>
            <option value="agreement">🤝 Service Agreement</option>
            <option value="policy">🔒 Privacy Policy</option>
            <option value="other">📋 Other Document</option>
          </select>
        </div>

        <div
          className={`drop-zone ${selectedFile ? 'has-file' : ''}`}
          onClick={handleButtonClick}
        >
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx,.txt"
            className="file-input"
          />

          {selectedFile ? (
            <div className="file-info">
              <span className="file-icon">📄</span>
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</p>
              <div className="file-status">
                <span className="status-indicator"></span>
                Ready for analysis
              </div>
            </div>
          ) : (
            <div className="drop-zone-content">
              <span className="upload-icon">📤</span>
              <p className="drop-zone-text">
                Click to select or drag and drop your document
              </p>
              <p className="drop-zone-hint">
                Supported formats: PDF, DOC, DOCX, TXT (Max 16MB)
              </p>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={!selectedFile || isLoading}
          className="submit-button"
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              Analyzing Document...
            </>
          ) : (
            'Run Compliance Audit'
          )}
        </button>
      </form>
    </div>
  );
};

export default AuditForm;
