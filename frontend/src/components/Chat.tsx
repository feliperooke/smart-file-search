import React from 'react';

interface ChatProps {
  isMobile?: boolean;
  onClose?: () => void;
}

interface MessageProps {
  content: string;
}

const QuestionMessage: React.FC<MessageProps> = ({ content }) => {
  return (
    <div className="flex justify-end">
      <div className="relative bg-gray-50 p-3 rounded-lg max-w-[80%]">
        <div className="absolute right-0 top-1/2 transform translate-x-1/2 -translate-y-1/2 rotate-45 w-3 h-3 bg-gray-50"></div>
        <p className="text-sm relative z-10">{content}</p>
      </div>
    </div>
  );
};

const AnswerMessage: React.FC<MessageProps> = ({ content }) => {
  return (
    <div className="flex justify-start">
      <div className="relative bg-blue-50 p-3 rounded-lg max-w-[80%]">
        <div className="absolute left-0 top-1/2 transform -translate-x-1/2 -translate-y-1/2 rotate-45 w-3 h-3 bg-blue-50"></div>
        <p className="text-sm relative z-10">{content}</p>
      </div>
    </div>
  );
};

export const Chat: React.FC<ChatProps> = ({ isMobile = false, onClose }) => {
  return (
    <div className={`${isMobile ? 'bg-white h-3/4 mt-auto rounded-t-xl' : 'bg-white shadow-lg rounded-sm h-full'} flex flex-col`}>
      <div className="bg-gray-50 border-b border-gray-200 px-4 py-2 text-sm text-gray-500 flex justify-between items-center">
        <span>Chat with your document</span>
        {isMobile && onClose && (
          <button onClick={onClose} className="text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      <div className="flex-grow p-4 overflow-auto">
        <div className="space-y-4">
          <AnswerMessage content="Hello! How can I help you with this document?" />
          <QuestionMessage content="I have a question about the content." />
        </div>
      </div>
      <div className="border-t border-gray-200 p-4 sticky bottom-0 bg-white">
        <div className="flex">
          <input 
            type="text" 
            placeholder="Type your message..." 
            className="flex-grow border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}; 