import React, { useState, useEffect } from 'react'
import { getHistory, deleteHistoryItems, saveHistoryItem } from '../utils/api'

const History = ({ onClose, onUseHistory, embedded = false }) => {
  const [historyItems, setHistoryItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('all')
  const [selectedItems, setSelectedItems] = useState(new Set())

  useEffect(() => {
    loadHistory()
  }, [filter])

  const loadHistory = async () => {
    setLoading(true)
    setError(null)
    
    const filters = filter === 'saved' ? { saved_only: true } : {}
    const result = await getHistory(1, 50, filters)
    
    if (result.success) {
      console.log('History items:', result.items)
      setHistoryItems(result.items)
    } else {
      setError(result.message)
    }
    
    setLoading(false)
  }

  const handleDelete = async () => {
    if (selectedItems.size === 0) return
    
    const ids = Array.from(selectedItems)
    const result = await deleteHistoryItems(ids)
    
    if (result.success) {
      setSelectedItems(new Set())
      loadHistory()
    } else {
      setError(result.message)
    }
  }

  const handleSave = async (historyId) => {
    const result = await saveHistoryItem(historyId)
    
    if (result.success) {
      loadHistory()
    } else {
      setError(result.message)
    }
  }

  const toggleSelection = (id) => {
    const newSelection = new Set(selectedItems)
    if (newSelection.has(id)) {
      newSelection.delete(id)
    } else {
      newSelection.add(id)
    }
    setSelectedItems(newSelection)
  }

  const formatDate = (dateString) => {
    try {
      // Parse as UTC by adding 'Z' if not present
      const utcString = dateString.endsWith('Z') ? dateString : dateString + 'Z'
      const itemDate = new Date(utcString)
      const now = new Date()
      
      const diffMs = now - itemDate
      const diffSecs = Math.floor(diffMs / 1000)
      const diffMins = Math.floor(diffSecs / 60)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)

      if (diffSecs < 10) return 'Just now'
      if (diffMins < 1) return `${diffSecs}s ago`
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      if (diffDays === 1) return 'Yesterday'
      if (diffDays < 7) return `${diffDays}d ago`
      
      return itemDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    } catch (e) {
      console.error('Date format error:', e, dateString)
      return 'Unknown'
    }
  }

  return (
    <div className={embedded ? 'hist-embed' : 'hist-modal-wrap'}>
      <div className={embedded ? 'hist-embed-content' : 'hist-modal'}>
        
        <div className="hist-filters">
          <button
            className={`hist-filter ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`hist-filter ${filter === 'saved' ? 'active' : ''}`}
            onClick={() => setFilter('saved')}
          >
            ⭐ Saved
          </button>
          
          {selectedItems.size > 0 && (
            <button onClick={handleDelete} className="hist-delete">
              🗑️ {selectedItems.size}
            </button>
          )}
        </div>

        {error && <div className="hist-error">⚠️ {error}</div>}

        {loading ? (
          <div className="hist-empty">
            <div className="hist-spinner"></div>
            <p>Loading...</p>
          </div>
        ) : historyItems.length === 0 ? (
          <div className="hist-empty">
            <div style={{fontSize: '48px', opacity: 0.5}}>📭</div>
            <p style={{fontSize: '16px', fontWeight: 600}}>No history</p>
            <p style={{fontSize: '13px', opacity: 0.7}}>Transformations appear here</p>
          </div>
        ) : (
          <div className="hist-list">
            {historyItems.map((item) => (
              <div key={item.id} className="hist-card">
                <div className="hist-top">
                  <input
                    type="checkbox"
                    checked={selectedItems.has(item.id)}
                    onChange={() => toggleSelection(item.id)}
                    style={{width: '18px', height: '18px', accentColor: '#667eea', cursor: 'pointer'}}
                  />
                  
                  <div className="hist-type">
                    {item.transformation_type.replace('_', ' ').toUpperCase()}
                  </div>
                  
                  <span className="hist-time">
                    {formatDate(item.created_at)}
                  </span>
                  
                  {item.is_saved && <span style={{fontSize: '16px'}}>⭐</span>}
                </div>

                <div className="hist-texts">
                  <div>
                    <div className="hist-label">ORIGINAL</div>
                    <div className="hist-text">{item.original_text}</div>
                  </div>
                  
                  <div style={{textAlign: 'center', color: '#667eea', fontSize: '18px', margin: '8px 0'}}>↓</div>
                  
                  <div>
                    <div className="hist-label">TRANSFORMED</div>
                    <div className="hist-text">{item.transformed_text}</div>
                  </div>
                </div>

                <div className="hist-actions">
                  <button onClick={() => onUseHistory(item)} className="hist-btn-use">
                    ↻ Use
                  </button>
                  
                  {!item.is_saved && (
                    <button onClick={() => handleSave(item.id)} className="hist-btn-save">
                      ⭐ Save
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default History