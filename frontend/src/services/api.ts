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