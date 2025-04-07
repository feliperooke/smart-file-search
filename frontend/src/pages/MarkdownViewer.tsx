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
    <div className="relative w-full h-full bg-[#f5f5f7]">
      {/* Main content with markdown viewer */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-6 p-6 h-full">
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
          <div className="backdrop-blur-xl bg-white/80 rounded-2xl shadow-sm h-full border border-white/20">
            <Chat />
          </div>
        </div>
      </div>

      {/* Mobile chat toggle button */}
      <button 
        onClick={toggleChat}
        className="md:hidden fixed bottom-6 right-6 bg-white/90 backdrop-blur-lg text-gray-800 p-3.5 rounded-full shadow-md z-10 border border-white/20"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>

      {/* Mobile chat overlay */}
      {isChatOpen && (
        <div className="md:hidden fixed inset-0 backdrop-blur-md bg-black/30 z-20 flex flex-col">
          <div className="bg-white/90 backdrop-blur-xl rounded-t-2xl shadow-lg h-3/4 mt-auto">
            <Chat isMobile={true} onClose={toggleChat} />
          </div>
        </div>
      )}
    </div>
  );
}; 