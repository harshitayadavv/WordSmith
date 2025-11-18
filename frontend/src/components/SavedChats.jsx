import React, { useState, useEffect } from 'react'
import { getHistory, deleteHistoryItems, saveHistoryItem } from '../utils/api'

const SavedChats = ({ onUseHistory }) => {
  const [savedItems, setSavedItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedItems, setSelectedItems] = useState(new Set())

  useEffect(() => {
    loadSavedChats()
  }, [])

  const loadSavedChats = async () => {
    setLoading(true)
    setError(null)
    
    // Get only saved items (no 7-day limit for saved)
    const result = await getHistory(1, 100, { saved_only: true })
    
    if (result.success) {
      console.log('Saved items:', result.items)
      setSavedItems(result.items)
    } else {
      setError(result.message)
    }
    
    setLoading(false)
  }

  const handleDelete = async () => {
    if (selectedItems.size === 0) return
    
    if (!confirm(`Delete ${selectedItems.size} saved item(s)?`)) return
    
    const ids = Array.from(selectedItems)
    const result = await deleteHistoryItems(ids)
    
    if (result.success) {
      setSelectedItems(new Set())
      loadSavedChats()
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
      const utcString = dateString.endsWith('Z') ? dateString : dateString + 'Z'
      const itemDate = new Date(utcString)
      
      return itemDate.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: itemDate.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
      })
    } catch (e) {
      return 'Unknown'
    }
  }

  const getTransformIcon = (type) => {
    const icons = {
      grammar_fix: '✏️',
      formal: '💼',
      friendly: '😊',
      shorten: '✂️',
      expand: '📝',
      bullet: '🔘',
      emoji: '😎',
      tweetify: '🐦'
    }
    return icons[type] || '📝'
  }

  return (
    <div className="saved-container">
      <div className="saved-header">
        <div className="saved-title">
          <span className="saved-icon">⭐</span>
          <h2>Saved Transformations</h2>
        </div>
        
        {selectedItems.size > 0 && (
          <button onClick={handleDelete} className="saved-delete-btn">
            🗑️ Delete {selectedItems.size}
          </button>
        )}
      </div>

      {error && <div className="saved-error">⚠️ {error}</div>}

      {loading ? (
        <div className="saved-loading">
          <div className="saved-spinner"></div>
          <p>Loading saved items...</p>
        </div>
      ) : savedItems.length === 0 ? (
        <div className="saved-empty">
          <div className="saved-empty-icon">⭐</div>
          <h3>No saved transformations yet</h3>
          <p>Save your favorite transformations from the History tab to keep them permanently!</p>
          <div className="saved-empty-steps">
            <div className="saved-step">
              <span className="step-number">1</span>
              <span>Transform text in the Chat tab</span>
            </div>
            <div className="saved-step">
              <span className="step-number">2</span>
              <span>Go to History and click ⭐ Save</span>
            </div>
            <div className="saved-step">
              <span className="step-number">3</span>
              <span>Find it here in Saved tab!</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="saved-list">
          <div className="saved-count">
            {savedItems.length} saved transformation{savedItems.length !== 1 ? 's' : ''}
          </div>
          
          {savedItems.map((item) => (
            <div key={item.id} className="saved-card">
              <div className="saved-card-header">
                <input
                  type="checkbox"
                  checked={selectedItems.has(item.id)}
                  onChange={() => toggleSelection(item.id)}
                  className="saved-checkbox"
                />
                
                <div className="saved-badge">
                  <span>{getTransformIcon(item.transformation_type)}</span>
                  <span>{item.transformation_type.replace('_', ' ').toUpperCase()}</span>
                </div>
                
                <span className="saved-date">
                  Saved on {formatDate(item.created_at)}
                </span>
              </div>

              <div className="saved-card-body">
                <div className="saved-section">
                  <div className="saved-label">ORIGINAL</div>
                  <div className="saved-content">{item.original_text}</div>
                </div>
                
                <div className="saved-arrow">→</div>
                
                <div className="saved-section">
                  <div className="saved-label">TRANSFORMED</div>
                  <div className="saved-content">{item.transformed_text}</div>
                </div>
              </div>

              <div className="saved-card-actions">
                <button
                  onClick={() => onUseHistory(item)}
                  className="saved-use-btn"
                >
                  ↻ Use Again
                </button>
                
                <button
                  onClick={async () => {
                    const result = await deleteHistoryItems([item.id])
                    if (result.success) loadSavedChats()
                  }}
                  className="saved-remove-btn"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SavedChats