import React, { useEffect, useState } from 'react';
import { useFile } from '../context/useFile';
import { sendChatMessage } from '../services/api';

interface ChatProps {
  isMobile?: boolean;
  onClose?: () => void;
}

interface MessageProps {
  content: string;
  delay?: number;
}

interface Message {
  type: 'question' | 'answer';
  content: string;
  delay: number;
}

const QuestionMessage: React.FC<MessageProps> = ({ content, delay = 0 }) => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [delay]);
  
  return (
    <div className="flex justify-end">
      <div 
        className={`relative bg-gray-800 p-3.5 rounded-2xl rounded-tr-sm max-w-[80%] shadow-sm 
          transition-all duration-500 ease-out
          ${isVisible 
            ? 'opacity-100 translate-y-0 scale-100' 
            : 'opacity-0 translate-y-4 scale-95'
          }`}
      >
        <p className="text-sm relative z-10 text-white">{content}</p>
      </div>
    </div>
  );
};

const AnswerMessage: React.FC<MessageProps> = ({ content, delay = 0 }) => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [delay]);
  
  return (
    <div className="flex justify-start">
      <div 
        className={`relative bg-[#E9E9EB] p-3.5 rounded-2xl rounded-tl-sm max-w-[80%] shadow-sm 
          transition-all duration-500 ease-out
          ${isVisible 
            ? 'opacity-100 translate-y-0 scale-100' 
            : 'opacity-0 translate-y-4 scale-95'
          }`}
      >
        <p className="text-sm relative z-10 text-gray-800">{content}</p>
      </div>
    </div>
  );
};

export const Chat: React.FC<ChatProps> = ({ isMobile = false, onClose }) => {
  const { fileRecord } = useFile();
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { type: 'answer', content: 'Hello! How can I help you with this document?', delay: 300 }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSendMessage = async () => {
    if (!inputValue.trim() || !fileRecord?.pk) return;
    
    const userMessage = inputValue.trim();
    
    // Add user message immediately
    const updatedMessages: Message[] = [
      ...messages,
      { type: 'question' as const, content: userMessage, delay: 0 }
    ];
    setMessages(updatedMessages);
    
    // Clear input
    setInputValue('');
    
    // Send to API and wait for response
    setIsLoading(true);
    try {
      const response = await sendChatMessage(fileRecord.pk.toString(), userMessage);
      
      if (response.error) {
        setMessages([
          ...updatedMessages,
          { type: 'answer' as const, content: `Error: ${response.error}`, delay: 300 }
        ]);
      } else {
        setMessages([
          ...updatedMessages,
          { type: 'answer' as const, content: response.content, delay: 300 }
        ]);
      }
    } catch {
      // Catch error but don't use the error variable
      setMessages([
        ...updatedMessages,
        { type: 'answer' as const, content: 'Sorry, there was an error processing your request.', delay: 300 }
      ]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendMessage();
    }
  };
  
  return (
    <div className={`${isMobile ? 'h-full' : 'h-full'} flex flex-col`}>
      <div className="px-4 py-3.5 flex justify-between items-center border-b border-gray-100">
        <span className="text-sm font-medium text-gray-700">Messages</span>
        {isMobile && onClose && (
          <button onClick={onClose} className="text-gray-500 rounded-full p-1 hover:bg-gray-100 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      <div className="flex-grow p-4 overflow-auto bg-white/50">
        <div className="space-y-4">
          {messages.map((message, index) => 
            message.type === 'answer' 
              ? <AnswerMessage key={index} content={message.content} delay={message.delay} />
              : <QuestionMessage key={index} content={message.content} delay={message.delay} />
          )}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-[#E9E9EB] p-3.5 rounded-2xl rounded-tl-sm shadow-sm flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-0"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-150"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-300"></div>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="border-t border-gray-100 p-4 sticky bottom-0 bg-white/90 backdrop-blur-sm">
        <div className="flex items-center">
          <input 
            type="text" 
            placeholder="Message"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading || !fileRecord}
            className="flex-grow bg-[#F5F5F7] border-none rounded-full px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-gray-600 text-sm disabled:bg-gray-100 disabled:text-gray-400"
          />
          <button 
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim() || !fileRecord}
            className={`ml-2 p-2 rounded-full transition-all duration-200 ${
              inputValue.trim() && !isLoading && fileRecord 
                ? 'bg-gray-800 text-white hover:bg-gray-700' 
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}; 