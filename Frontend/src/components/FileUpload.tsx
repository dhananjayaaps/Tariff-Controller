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
    <div id="upload" className="mb-6">
      <h2 className="text-xl font-bold mb-2">File Upload</h2>
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="border-2 border-dashed border-gray-300 p-6 text-center bg-gray-100 rounded-lg hover:bg-gray-200 transition"
      >
        <p className="text-gray-600">Drag and Drop CSV/Excel file here</p>
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={(e) => e.target.files && handleUpload(e.target.files[0])}
          className="mt-2"
        />
      </div>
      {message && <p className="mt-2 text-green-600">{message}</p>}
    </div>
  );
};

export default FileUpload;