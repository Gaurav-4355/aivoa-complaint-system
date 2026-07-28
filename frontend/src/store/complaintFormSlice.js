import { createSlice } from '@reduxjs/toolkit'

const emptyFields = {
  complaint_source: '',
  customer_name: '',
  product_name: '',
  product_strength_grade: '',
  batch_lot_number: '',
  manufacturing_date: '',
  expiry_date: '',
  quantity_affected: '',
  complaint_type: '',
  complaint_date: '',
  detailed_description: '',
}

const initialState = {
  fields: emptyFields,
  initial_severity: '',
  priority: '',
  status: 'awaiting_extraction', // awaiting_extraction | populated | saved
  completeness_status: null,
  missing_fields: [],
  duplicate_of_ids: [],
  root_cause_suggestion: '',
  capa_suggestion: '',
  ai_summary: '',
  risk_classification: '',
}

const complaintFormSlice = createSlice({
  name: 'complaintForm',
  initialState,
  reducers: {
    fieldChanged(state, action) {
      const { field, value } = action.payload
      state.fields[field] = value
    },
    populatedFromExtraction(state, action) {
      const r = action.payload
      state.fields = { ...state.fields, ...r.extracted_fields }
      state.initial_severity = r.initial_severity
      state.priority = r.priority
      state.completeness_status = r.completeness_status
      state.missing_fields = r.missing_fields
      state.duplicate_of_ids = r.duplicate_of_ids
      state.root_cause_suggestion = r.root_cause_suggestion
      state.capa_suggestion = r.capa_suggestion
      state.ai_summary = r.ai_summary
      state.risk_classification = r.risk_classification
      state.status = 'populated'
    },
    formReset() {
      return initialState
    },
    markSaved(state) {
      state.status = 'saved'
    },
  },
})

export const { fieldChanged, populatedFromExtraction, formReset, markSaved } =
  complaintFormSlice.actions
export default complaintFormSlice.reducer
