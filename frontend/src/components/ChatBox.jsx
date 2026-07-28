import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { askAssistant } from '../api/client'
import { messageAdded } from '../store/aiAssistantSlice'

export default function ChatBox() {
  const dispatch = useDispatch()
  const messages = useSelector((s) => s.aiAssistant.messages)
  const fields = useSelector((s) => s.complaintForm.fields)
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)

  const onSend = async () => {
    if (!input.trim()) return
    const question = input
    dispatch(messageAdded({ role: 'user', text: question }))
    setInput('')
    setSending(true)
    try {
      const { answer } = await askAssistant(question, fields)
      dispatch(messageAdded({ role: 'assistant', text: answer }))
    } catch (err) {
      dispatch(messageAdded({ role: 'assistant', text: 'Sorry, something went wrong.' }))
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="chatbox">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble chat-${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>
      <div className="chat-input-row">
        <input
          value={input}
          placeholder="Ask me anything about this complaint..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSend()}
        />
        <button onClick={onSend} disabled={sending}>
          Send
        </button>
      </div>
      <p className="hint">AI responses may contain errors. Please verify information.</p>
    </div>
  )
}
