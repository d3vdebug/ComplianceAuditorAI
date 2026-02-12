import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import AuditForm from './components/AuditForm';
import Results from './components/Results';

export interface AuditResult {
  documentName: string;
  complianceScore: number;
  issues: string[];
  passedChecks: string[];
  timestamp: string;
}

function App() {
  const [auditResults, setAuditResults] = useState<AuditResult | null>(null);

  const handleAuditComplete = (results: any) => {
    setAuditResults(results);
  };

  return (
    <div className="App">
      <Header />
      <main className="main-content">
        <AuditForm onAuditComplete={handleAuditComplete} />
        {auditResults && <Results result={auditResults} />}
      </main>
    </div>
  );
}

export default App;
