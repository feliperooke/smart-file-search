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

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = filename || 'document.md';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="backdrop-blur-xl bg-white/90 rounded-2xl shadow-sm h-full flex flex-col border border-white/20 overflow-hidden">
      {/* Document header with filename */}
      <div className="backdrop-blur-sm bg-white/80 px-8 py-3.5 text-sm font-medium text-gray-700 flex items-center justify-between">
        <span className="truncate">{filename || 'Untitled Document'}</span>
        <button 
          onClick={handleDownload}
          className="bg-white/90 border border-gray-300 text-gray-400 transition-colors p-1.5 rounded-full hover:bg-gray-700 hover:text-white hover:border-transparent shadow-sm"
          aria-label="Download document"
          title="Download"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
      
      {/* Main content area */}
      <div className="px-16 py-12 overflow-auto flex-grow bg-white/70">
        <MarkdownRenderer content={content} />
      </div>

      {/* Document footer */}
      <div className="backdrop-blur-sm bg-white/80 px-8 py-3 text-xs text-gray-500 flex justify-between">
        <span>Smart File Search</span>
        <span>{createdAt ? formatDate(createdAt) : ''}</span>
      </div>
    </div>
  );
}; 