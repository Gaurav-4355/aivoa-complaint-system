import { configureStore } from '@reduxjs/toolkit'
import complaintFormReducer from './complaintFormSlice'
import aiAssistantReducer from './aiAssistantSlice'

export const store = configureStore({
  reducer: {
    complaintForm: complaintFormReducer,
    aiAssistant: aiAssistantReducer,
  },
})
