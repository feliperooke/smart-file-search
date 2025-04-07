import { FileRecord } from '../context/fileContextTypes';

export const uploadFile = async (file: File): Promise<FileRecord> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:8000/api/process', {
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
  sources?: {
    page: number;
    text: string;
  }[];
  error?: string;
}

export const sendChatMessage = async (fileId: string, message: string): Promise<ChatResponse> => {
  try {
    const response = await fetch('http://localhost:8000/api/chat/', {
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

    return response.json();
  } catch (error) {
    if (error instanceof Error) {
      return {
        answer: '',
        error: `Failed to send message: ${error.message}`
      };
    }
    return {
      answer: '',
      error: 'Failed to send message: Unknown error'
    };
  }
}; 