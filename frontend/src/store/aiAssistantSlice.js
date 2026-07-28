import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  extractionProgress: 0, // 0-100
  isExtracting: false,
  error: null,
  messages: [
    {
      role: 'assistant',
      text: 'Upload a complaint document or paste text above. I will automatically extract the details and populate the form for you.',
    },
  ],
}

const aiAssistantSlice = createSlice({
  name: 'aiAssistant',
  initialState,
  reducers: {
    extractionStarted(state) {
      state.isExtracting = true
      state.extractionProgress = 10
      state.error = null
    },
    extractionProgressed(state, action) {
      state.extractionProgress = action.payload
    },
    extractionFinished(state) {
      state.isExtracting = false
      state.extractionProgress = 100
    },
    extractionFailed(state, action) {
      state.isExtracting = false
      state.error = action.payload
    },
    messageAdded(state, action) {
      state.messages.push(action.payload)
    },
  },
})

export const {
  extractionStarted,
  extractionProgressed,
  extractionFinished,
  extractionFailed,
  messageAdded,
} = aiAssistantSlice.actions
export default aiAssistantSlice.reducer
