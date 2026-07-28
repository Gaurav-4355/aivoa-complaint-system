import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

export async function extractFromFile(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/complaints/extract', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function extractFromText(text) {
  const form = new FormData()
  form.append('text', text)
  const { data } = await api.post('/complaints/extract', form)
  return data
}

export async function saveComplaint(payload) {
  const { data } = await api.post('/complaints', payload)
  return data
}

export async function askAssistant(question, context) {
  const { data } = await api.post('/chat', { question, context })
  return data
}

export default api
