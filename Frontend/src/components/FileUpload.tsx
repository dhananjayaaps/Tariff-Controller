"use client";
import { useState } from 'react';
import { uploadFile } from '../utils/api';

const FileUpload = () => {
  const [message, setMessage] = useState<string | null>(null);

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  const handleUpload = async (file: File) => {
    try {
      const response = await uploadFile(file);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Upload failed');
    }
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      style={{ border: '2px dashed #ccc', padding: '20px', textAlign: 'center' }}
    >
      Drag and Drop CSV/Excel file here
      <input
        type="file"
        accept=".csv,.xlsx"
        onChange={(e) => e.target.files && handleUpload(e.target.files[0])}
        style={{ marginTop: '10px' }}
      />
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;