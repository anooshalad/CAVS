import React from 'react';
import type { AnalysisResult } from '../App';

interface ResultCardProps {
  data: AnalysisResult;
}

const FIELD_LABELS: Record<string, string> = {
  product_name: 'Product Name',
  dosage: 'Dosage',
  batch_number: 'Batch Number',
  expiry_date: 'Expiry Date',
};

const ResultCard: React.FC<ResultCardProps> = ({ data }) => {
  const { raw_text, fields, validation, status } = data;

  return (
    <div className="result-card">
      <h2>
        Analysis Result{' '}
        <span className={`badge ${status === 'PASS' ? 'pass' : 'fail'}`}>
          {status === 'PASS' ? '✅ COMPLIANT' : '❌ NON-COMPLIANT'}
        </span>
      </h2>

      <section className="fields">
        <h3>Extracted Fields</h3>
        <table>
          <thead>
            <tr>
              <th>Field</th>
              <th>Extracted Value</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {validation.map((check, idx) => (
              <tr key={idx}>
                <td>{FIELD_LABELS[check.field] || check.field}</td>
                <td>{(fields as any)[check.field] || '—'}</td>
                <td>
                  <span className={`badge ${check.status === 'PASS' ? 'pass' : 'fail'}`}>
                    {check.status === 'PASS' ? '✅ PASS' : '❌ FAIL'}
                  </span>
                  <div className="msg">{check.message}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="raw-text">
        <h3>Raw OCR Text</h3>
        <pre>{raw_text}</pre>
      </section>
    </div>
  );
};

export default ResultCard;
