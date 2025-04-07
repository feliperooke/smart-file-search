import { useNavigate } from 'react-router-dom';
import { FileUploader } from '../components/FileUploader';
import { useFile } from '../context/useFile';
import { FileRecord } from '../context/fileContextTypes';

export const Home = () => {
  const navigate = useNavigate();
  const { setFileRecord } = useFile();

  const handleFileUploaded = (fileRecord: FileRecord) => {
    setFileRecord(fileRecord);
    navigate('/markdown');
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-3xl px-8 py-12 bg-white rounded-2xl shadow-lg">
        <h1 className="text-4xl font-medium text-center text-gray-900 mb-6">
          Smart File Search
        </h1>
        <p className="text-center text-gray-500 text-lg mb-10 max-w-xl mx-auto">
          Upload your file and we'll intelligently extract its content for you
        </p>
        <div className="mx-auto max-w-lg">
          <FileUploader onFileUploaded={handleFileUploaded} />
        </div>
      </div>
      <div className="mt-8 text-sm text-gray-400">
        Simple. Powerful. Intuitive.
      </div>
    </div>
  );
}; 