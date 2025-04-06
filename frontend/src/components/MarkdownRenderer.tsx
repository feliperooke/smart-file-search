import React from 'react';
import ReactMarkdown from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="prose prose-slate max-w-none">
      <ReactMarkdown
        components={{
          h1: ({ children }) => <h1 className="text-2xl font-bold mb-6">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold mb-4">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-medium mb-3">{children}</h3>,
          p: ({ children }) => <p className="mb-4 leading-relaxed">{children}</p>,
          ul: ({ children }) => <ul className="list-disc pl-6 mb-4">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal pl-6 mb-4">{children}</ol>,
          li: ({ children }) => <li className="mb-2">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-gray-200 pl-4 italic my-4">{children}</blockquote>
          ),
          code: ({ children }) => (
            <code className="bg-gray-50 px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>
          ),
          pre: ({ children }) => (
            <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto my-4">{children}</pre>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}; 