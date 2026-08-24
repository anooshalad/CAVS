import React, { useState } from 'react';

interface UploadPanelProps {
  onUpload: (file: File) => Promise<void>;
  loading: boolean;
}

const UploadPanel: React.FC<UploadPanelProps> = ({ onUpload, loading }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedFile) {
      await onUpload(selectedFile);
    }
  };

  return (
    <form className="upload-panel" onSubmit={handleSubmit}>
      <label className="file-input-label">
        <input type="file" accept="image/*,application/pdf" onChange={handleChange} disabled={loading} />
        <span>{loading ? 'Processing…' : 'Choose file'}</span>
      </label>
      {previewUrl && (
        <div className="preview">
          <img src={previewUrl} alt="preview" className="preview-img" />
        </div>
      )}
      <button type="submit" disabled={!selectedFile || loading} className="upload-button">
        {loading ? 'Analyzing…' : 'Upload & Analyze'}
      </button>
    </form>
  );
};

export default UploadPanel;
