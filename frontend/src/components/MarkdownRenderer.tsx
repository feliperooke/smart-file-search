import React from 'react';
import ReactMarkdown from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="prose prose-slate max-w-none font-['SF_Pro_Display',system-ui,sans-serif]">
      <ReactMarkdown
        components={{
          h1: ({ children }) => <h1 className="text-3xl font-semibold mb-6 tracking-tight text-gray-900">{children}</h1>,
          h2: ({ children }) => <h2 className="text-2xl font-semibold mb-5 tracking-tight text-gray-900">{children}</h2>,
          h3: ({ children }) => <h3 className="text-xl font-medium mb-4 tracking-tight text-gray-900">{children}</h3>,
          p: ({ children }) => <p className="mb-5 leading-relaxed text-[15px] text-gray-800">{children}</p>,
          ul: ({ children }) => <ul className="list-disc pl-6 mb-5 text-[15px] text-gray-800">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal pl-6 mb-5 text-[15px] text-gray-800">{children}</ol>,
          li: ({ children }) => <li className="mb-2.5">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-gray-300 pl-5 italic my-5 text-gray-700">{children}</blockquote>
          ),
          code: ({ children }) => (
            <code className="bg-[#F5F5F7] px-1.5 py-0.5 rounded-md text-sm font-mono text-gray-800">{children}</code>
          ),
          pre: ({ children }) => (
            <pre className="bg-[#F5F5F7] p-4 rounded-lg overflow-x-auto my-5 shadow-sm">{children}</pre>
          ),
          a: ({ href, children }) => (
            <a href={href} className="text-[#007AFF] no-underline hover:underline transition-colors">{children}</a>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}; 