import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { MarkdownViewer } from './pages/MarkdownViewer'
import { FileProvider } from './context/FileContext'

function App() {
  return (
    <FileProvider>
      <BrowserRouter>
        <div>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/markdown" element={<MarkdownViewer />} />
          </Routes>
        </div>
      </BrowserRouter>
    </FileProvider>
  )
}

export default App
