import { useSelector, useDispatch } from 'react-redux'
import { fieldChanged, formReset, markSaved } from '../store/complaintFormSlice'
import { saveComplaint } from '../api/client'

const FIELD_GROUPS = [
  {
    title: '1. Origin & customer details',
    fields: [
      ['complaint_source', 'Complaint source'],
      ['customer_name', 'Customer name'],
    ],
  },
  {
    title: '2. Product & batch identification',
    fields: [
      ['product_name', 'Product name'],
      ['product_strength_grade', 'Product strength / grade'],
      ['batch_lot_number', 'Batch / lot number'],
      ['manufacturing_date', 'Manufacturing date'],
      ['expiry_date', 'Expiry date'],
      ['quantity_affected', 'Quantity affected'],
    ],
  },
  {
    title: '3. Complaint details',
    fields: [
      ['complaint_type', 'Complaint type'],
      ['complaint_date', 'Complaint date'],
    ],
  },
]

export default function ComplaintForm() {
  const dispatch = useDispatch()
  const form = useSelector((s) => s.complaintForm)

  const onChange = (field) => (e) =>
    dispatch(fieldChanged({ field, value: e.target.value }))

  const onSave = async () => {
    await saveComplaint({
      ...form.fields,
      initial_severity: form.initial_severity,
      priority: form.priority,
      completeness_status: form.completeness_status,
      missing_fields: form.missing_fields,
      duplicate_of_ids: form.duplicate_of_ids,
      root_cause_suggestion: form.root_cause_suggestion,
      capa_suggestion: form.capa_suggestion,
      ai_summary: form.ai_summary,
      risk_classification: form.risk_classification,
    })
    dispatch(markSaved())
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Log customer complaint</h2>
          <p className="subtitle">API & PDF quality assurance module</p>
        </div>
        <span className={`badge badge-${form.status}`}>
          {form.status.replace('_', ' ')}
        </span>
      </div>

      {form.completeness_status === 'incomplete' && (
        <div className="notice notice-warning">
          Missing fields: {form.missing_fields.join(', ')}
        </div>
      )}
      {form.duplicate_of_ids.length > 0 && (
        <div className="notice notice-warning">
          Possible duplicate of complaint id(s): {form.duplicate_of_ids.join(', ')}
        </div>
      )}
      {form.ai_summary && <div className="notice notice-info">{form.ai_summary}</div>}

      {FIELD_GROUPS.map((group) => (
        <div className="field-group" key={group.title}>
          <h3>{group.title}</h3>
          <div className="field-grid">
            {group.fields.map(([key, label]) => (
              <label key={key} className="field">
                <span>{label}</span>
                <input
                  value={form.fields[key] || ''}
                  placeholder="Awaiting AI extraction..."
                  onChange={onChange(key)}
                />
              </label>
            ))}
          </div>
        </div>
      ))}

      <div className="field-group">
        <h3>Detailed complaint description</h3>
        <textarea
          rows={4}
          value={form.fields.detailed_description || ''}
          placeholder="Awaiting AI extraction..."
          onChange={onChange('detailed_description')}
        />
      </div>

      <div className="field-group">
        <h3>4. Initial assessment & priority</h3>
        <div className="field-grid">
          <label className="field">
            <span>Initial severity</span>
            <select
              value={form.initial_severity}
              onChange={(e) =>
                dispatch(fieldChanged({ field: 'initial_severity', value: e.target.value }))
              }
            >
              <option value="">Awaiting AI extraction...</option>
              <option>Critical</option>
              <option>Major</option>
              <option>Minor</option>
            </select>
          </label>
          <label className="field">
            <span>Priority</span>
            <select
              value={form.priority}
              onChange={(e) =>
                dispatch(fieldChanged({ field: 'priority', value: e.target.value }))
              }
            >
              <option value="">Awaiting AI extraction...</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </label>
        </div>
      </div>

      <div className="actions">
        <button className="btn-secondary" onClick={() => dispatch(formReset())}>
          Reset form
        </button>
        <button className="btn-primary" onClick={onSave}>
          Save complaint
        </button>
      </div>
    </div>
  )
}
