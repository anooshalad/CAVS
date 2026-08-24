import React, { useState } from 'react';
import UploadPanel from './components/UploadPanel';
import ResultCard from './components/ResultCard';
import './index.css';

export interface ValidationCheck {
  field: string;
  status: string;
  message: string;
}

export interface AnalysisResult {
  submission_id: string;
  status: string;
  fields: {
    product_name: string | null;
    dosage: string | null;
    batch_number: string | null;
    expiry_date: string | null;
  };
  validation: ValidationCheck[];
  raw_text: string;
}

const App: React.FC = () => {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    try {
      const submissionId = crypto.randomUUID();
      const form = new FormData();
      form.append('file', file);

      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/submissions/${submissionId}/analyze`, {
        method: 'POST',
        body: form,
      });
      if (!response.ok) {
        const txt = await response.text();
        throw new Error(`Server error ${response.status}: ${txt}`);
      }
      const data: AnalysisResult = await response.json();
      setAnalysis(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>CAVS</h1>
        <p>Pharmaceutical Artwork Compliance Verification</p>
      </header>
      <main className="main-content">
        <UploadPanel onUpload={handleUpload} loading={loading} />
        {error && <div className="error">{error}</div>}
        {analysis && <ResultCard data={analysis} />}
      </main>
    </div>
  );
};

export default App;
