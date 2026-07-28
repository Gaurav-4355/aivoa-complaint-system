import { useRef, useState } from 'react'
import { useDispatch } from 'react-redux'
import { extractFromFile, extractFromText } from '../api/client'
import { populatedFromExtraction } from '../store/complaintFormSlice'
import {
  extractionStarted,
  extractionProgressed,
  extractionFinished,
  extractionFailed,
} from '../store/aiAssistantSlice'

export default function FileUpload() {
  const dispatch = useDispatch()
  const inputRef = useRef(null)
  const [pastedText, setPastedText] = useState('')

  const runExtraction = async (fn) => {
    dispatch(extractionStarted())
    const tick = setInterval(
      () => dispatch(extractionProgressed(Math.min(90, Math.random() * 80 + 10))),
      400
    )
    try {
      const result = await fn()
      dispatch(populatedFromExtraction(result))
      dispatch(extractionFinished())
    } catch (err) {
      dispatch(extractionFailed(err.message))
    } finally {
      clearInterval(tick)
    }
  }

  const onDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) runExtraction(() => extractFromFile(file))
  }

  const onBrowse = (e) => {
    const file = e.target.files?.[0]
    if (file) runExtraction(() => extractFromFile(file))
  }

  const onPasteSubmit = () => {
    if (pastedText.trim()) runExtraction(() => extractFromText(pastedText))
  }

  return (
    <div>
      <div
        className="dropzone"
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
      >
        <p>Drag & drop complaint document here</p>
        <span>or click to browse</span>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt,.eml"
          hidden
          onChange={onBrowse}
        />
      </div>

      <div className="divider">OR</div>

      <textarea
        className="paste-box"
        rows={3}
        placeholder="Paste complaint text / email"
        value={pastedText}
        onChange={(e) => setPastedText(e.target.value)}
      />
      <button className="btn-secondary full-width" onClick={onPasteSubmit}>
        Extract from pasted text
      </button>

      <p className="hint">Supported formats: PDF, DOCX, TXT, EML. Max size 10MB.</p>
    </div>
  )
}
