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
    <div className="w-full mx-auto">
      <div
        className={`border-[1px] rounded-xl p-10 text-center transition-all duration-200 shadow-sm ${
          isDragging 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-200 bg-gray-50 hover:border-gray-300'
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
            className="w-14 h-14 text-gray-400 mb-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <span className="text-lg font-light text-gray-600 mb-2">
            Drag and drop your file here
          </span>
          <span className="inline-block px-5 py-2 mt-2 bg-gray-800 text-white text-sm font-medium rounded-full transition-all hover:bg-gray-700">
            Browse Files
          </span>
        </label>
      </div>

      {isLoading && (
        <div className="mt-6 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-2 border-gray-300 border-t-gray-800"></div>
          <p className="mt-3 text-gray-500 font-light">Processing your file...</p>
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-50 text-red-500 rounded-xl border border-red-100">
          <p className="font-medium">Error</p>
          <p className="mt-1 font-light">{error}</p>
        </div>
      )}

      {fileName && !isLoading && !error && (
        <div className="mt-6 p-4 bg-gray-50 border border-gray-200 text-gray-700 rounded-xl flex items-center">
          <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="font-light">{fileName}</span>
        </div>
      )}
    </div>
  );
}; 