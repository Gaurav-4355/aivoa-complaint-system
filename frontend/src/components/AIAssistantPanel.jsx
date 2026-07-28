import { useSelector } from 'react-redux'
import FileUpload from './FileUpload'
import ChatBox from './ChatBox'

export default function AIAssistantPanel() {
  const { extractionProgress, isExtracting } = useSelector((s) => s.aiAssistant)

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>AI complaint intake assistant</h2>
        <span className="badge badge-beta">Beta</span>
      </div>

      <FileUpload />

      {isExtracting && (
        <div className="progress-section">
          <div className="progress-label">
            <span>Extraction progress</span>
            <span>{Math.round(extractionProgress)}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${extractionProgress}%` }} />
          </div>
          <p className="hint">Analyzing document content and extracting key details...</p>
        </div>
      )}

      <div className="ai-assistant-label">AI assistant</div>
      <ChatBox />
    </div>
  )
}
