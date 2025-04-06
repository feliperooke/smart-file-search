import React, { useState, ReactNode, useMemo, useEffect } from 'react';
import { FileContext, FileRecord } from './fileContextTypes';

const STORAGE_KEY = 'fileRecord';

const loadFileRecord = (): FileRecord | null => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch (error) {
      console.error('Error parsing stored file record:', error);
      return null;
    }
  }
  return null;
};

const saveFileRecord = (fileRecord: FileRecord | null) => {
  if (fileRecord) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(fileRecord));
  } else {
    localStorage.removeItem(STORAGE_KEY);
  }
};

export const FileProvider = ({ children }: { children: ReactNode }) => {
  const [fileRecord, setFileRecord] = useState<FileRecord | null>(() => loadFileRecord());

  useEffect(() => {
    saveFileRecord(fileRecord);
  }, [fileRecord]);

  const value = useMemo(() => ({ fileRecord, setFileRecord }), [fileRecord]);

  return (
    <FileContext.Provider value={value}>
      {children}
    </FileContext.Provider>
  );
}; 