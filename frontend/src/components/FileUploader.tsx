import { useState, useCallback } from 'react';
import { uploadFile } from '../services/api';
import { FileRecord } from '../context/fileContextTypes';

interface FileUploaderProps {
  onFileUploaded: (fileRecord: FileRecord) => void;
}

export const FileUploader = ({ onFileUploaded }: FileUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      await handleFileUpload(file);
    }
  }, []);

  const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await handleFileUpload(file);
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    try {
      setIsLoading(true);
      setError(null);
      setFileName(file.name);

      console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type);
      
      const fileRecord = await uploadFile(file);
      console.log('Upload response:', fileRecord);
      
      onFileUploaded(fileRecord);
    } catch (error) {
      console.error('Upload error:', error);
      setError(error instanceof Error ? error.message : 'Failed to upload file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          onChange={handleFileSelect}
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <svg
            className="w-12 h-12 text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <span className="text-lg font-medium text-gray-600">
            Drag and drop your file here, or click to select
          </span>
        </label>
      </div>

      {isLoading && (
        <div className="mt-4 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
          <p className="mt-2 text-gray-600">Uploading...</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-lg">
          <p className="font-medium">Error:</p>
          <p className="mt-1">{error}</p>
        </div>
      )}

      {fileName && !isLoading && !error && (
        <div className="mt-4 p-4 bg-green-50 text-green-600 rounded-lg">
          File uploaded: {fileName}
        </div>
      )}
    </div>
  );
}; 