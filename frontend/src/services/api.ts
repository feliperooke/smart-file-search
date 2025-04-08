import { FileRecord } from '../context/fileContextTypes';

// API base URL from environment variables with trailing slashes removed
const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export const uploadFile = async (file: File): Promise<FileRecord> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/api/process`, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
      },
      mode: 'cors',
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`Upload failed: ${errorData}`);
    }

    return response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Upload failed: ${error.message}`);
    }
    throw new Error('Upload failed: Unknown error');
  }
};

interface ChatResponse {
  answer: string;
  content?: string;
  sources?: {
    page: number;
    text: string;
  }[];
  error?: string;
}

export const sendChatMessage = async (fileId: string, message: string): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_URL}/api/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        pk: fileId,
        search: message
      }),
      mode: 'cors',
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`Chat request failed: ${errorData}`);
    }

    const data = await response.json();
    // Ensure content property is set
    data.content = data.content || data.answer;
    return data;
  } catch (error) {
    if (error instanceof Error) {
      return {
        answer: '',
        content: '',
        error: `Failed to send message: ${error.message}`
      };
    }
    return {
      answer: '',
      content: '',
      error: 'Failed to send message: Unknown error'
    };
  }
}; 