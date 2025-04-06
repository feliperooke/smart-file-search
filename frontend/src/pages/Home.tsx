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
    <div className="h-screen w-screen bg-gray-50 flex flex-col items-center justify-center">
      <div className="w-full max-w-4xl px-4">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Smart File Search
        </h1>
        <p className="text-center text-gray-600 mb-12">
          Upload your file and we'll extract its content for you
        </p>
        <FileUploader onFileUploaded={handleFileUploaded} />
      </div>
    </div>
  );
}; 