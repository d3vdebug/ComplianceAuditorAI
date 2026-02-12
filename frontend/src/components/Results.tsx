import React from 'react';
import './Results.css';
import { AuditResult } from '../App';

interface ResultsProps {
  result: AuditResult;
}

const Results: React.FC<ResultsProps> = ({ result }) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return '#48bb78';
    if (score >= 70) return '#ed8936';
    return '#f56565';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return 'Excellent';
    if (score >= 80) return 'Good';
    if (score >= 70) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="results-container">
      <h2 className="results-title">Audit Results</h2>
      
      <div className="document-info">
        <p className="document-name">
          <strong>Document:</strong> {result.documentName}
        </p>
        <p className="timestamp">
          <strong>Audited:</strong> {new Date(result.timestamp).toLocaleString()}
        </p>
      </div>

      <div className="score-section">
        <div className="score-circle" style={{ borderColor: getScoreColor(result.complianceScore) }}>
          <span className="score-value">{result.complianceScore}</span>
          <span className="score-label">{getScoreLabel(result.complianceScore)}</span>
        </div>
        <p className="score-description">Compliance Score</p>
      </div>

      <div className="results-grid">
        <div className="result-card issues-card">
          <h3 className="card-title">
            <span className="icon">⚠️</span>
            Issues Found ({result.issues.length})
          </h3>
          <ul className="result-list">
            {result.issues.map((issue, index) => (
              <li key={index} className="result-item issue-item">
                {issue}
              </li>
            ))}
          </ul>
        </div>

        <div className="result-card passed-card">
          <h3 className="card-title">
            <span className="icon">✅</span>
            Passed Checks ({result.passedChecks.length})
          </h3>
          <ul className="result-list">
            {result.passedChecks.map((check, index) => (
              <li key={index} className="result-item passed-item">
                {check}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Results;
