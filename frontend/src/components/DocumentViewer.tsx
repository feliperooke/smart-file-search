import React from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface DocumentViewerProps {
  filename: string;
  content: string;
  createdAt?: string;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({ 
  filename, 
  content, 
  createdAt 
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="bg-white shadow-lg rounded-sm h-full flex flex-col">
      {/* PDF-like header with filename */}
      <div className="bg-gray-50 border-b border-gray-200 px-8 py-2 text-sm text-gray-500">
        {filename || 'Untitled Document'}
      </div>
      
      {/* Main content area */}
      <div className="px-16 py-12 overflow-auto flex-grow">
        <MarkdownRenderer content={content} />
      </div>

      {/* PDF-like footer */}
      <div className="bg-gray-50 border-t border-gray-200 px-8 py-2 text-sm text-gray-500 flex justify-between">
        <span>Smart File Search</span>
        <span>{createdAt ? formatDate(createdAt) : ''}</span>
      </div>
    </div>
  );
}; 