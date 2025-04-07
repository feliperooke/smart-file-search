import { createContext } from 'react';

export interface FileRecord {
  pk: number;
  filename: string;
  url: string;
  content: string;
  file_size: number;
  file_type: string;
  markdown_content: string;
  processing_status: string;
  embedding_status: string;
  created_at: string;
  updated_at: string;
  error_message: string | null;
  metadata: Record<string, string | number | boolean>;
  history: Record<string, unknown>;
}

export interface FileContextType {
  fileRecord: FileRecord | null;
  setFileRecord: (fileRecord: FileRecord | null) => void;
}

export const FileContext = createContext<FileContextType | undefined>(undefined); 