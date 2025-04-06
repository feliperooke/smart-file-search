import { useState } from 'react';
import { useFile } from '../context/useFile';
import { DocumentViewer } from '../components/DocumentViewer';
import { Chat } from '../components/Chat';

export const MarkdownViewer = () => {
  const { fileRecord } = useFile();
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="relative h-full">
      {/* Main content with markdown viewer */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4 p-4 h-full">
        {/* Markdown content - takes full width on mobile, 4 columns on desktop */}
        <div className="col-span-1 md:col-span-4">
          <DocumentViewer 
            filename={fileRecord?.filename || 'Untitled Document'}
            content={fileRecord?.markdown_content || ''}
            createdAt={fileRecord?.created_at}
          />
        </div>

        {/* Chat section - hidden on mobile by default, shown on desktop */}
        <div className="hidden md:block md:col-span-2">
          <Chat />
        </div>
      </div>

      {/* Mobile chat toggle button */}
      <button 
        onClick={toggleChat}
        className="md:hidden fixed bottom-4 right-4 bg-blue-500 text-white p-3 rounded-full shadow-lg z-10"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>

      {/* Mobile chat overlay */}
      {isChatOpen && (
        <div className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-20 flex flex-col">
          <Chat isMobile={true} onClose={toggleChat} />
        </div>
      )}
    </div>
  );
}; 