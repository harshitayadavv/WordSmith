import React from 'react'

const TransformButtons = ({ selectedTransforms, onTransformSelect }) => {
  const transforms = [
    { id: 'grammar', label: 'Grammar Fix', icon: '✏️', category: 'neutral' },
    { id: 'formal', label: 'Formal', icon: '💼', category: 'tone' },
    { id: 'friendly', label: 'Friendly', icon: '😊', category: 'tone' },
    { id: 'shorten', label: 'Shorten', icon: '✂️', category: 'length' },
    { id: 'expand', label: 'Expand', icon: '📝', category: 'length' },
    { id: 'bullet', label: 'Bullet', icon: '🔘', category: 'neutral' },
    { id: 'emoji', label: 'Emoji', icon: '😎', category: 'neutral' },
    { id: 'tweetify', label: 'Tweetify', icon: '🐦', category: 'neutral' },
  ]

  // Check if a transform conflicts with currently selected ones
  const hasConflict = (transformId) => {
    const transform = transforms.find(t => t.id === transformId)
    
    // If trying to select a tone transformation
    if (transform.category === 'tone') {
      // Check if opposite tone is already selected
      const conflictingTones = transforms
        .filter(t => t.category === 'tone' && t.id !== transformId)
        .map(t => t.id)
      
      return selectedTransforms.some(id => conflictingTones.includes(id))
    }
    
    // If trying to select a length transformation
    if (transform.category === 'length') {
      // Check if opposite length is already selected
      const conflictingLengths = transforms
        .filter(t => t.category === 'length' && t.id !== transformId)
        .map(t => t.id)
      
      return selectedTransforms.some(id => conflictingLengths.includes(id))
    }
    
    return false
  }

  const handleTransformClick = (transformId) => {
    // Check if already selected
    const isSelected = selectedTransforms.includes(transformId)
    
    if (isSelected) {
      // Deselect
      onTransformSelect(selectedTransforms.filter(id => id !== transformId))
    } else {
      // Check for conflicts
      if (hasConflict(transformId)) {
        // Remove conflicting transforms and add new one
        const transform = transforms.find(t => t.id === transformId)
        const filtered = selectedTransforms.filter(id => {
          const selectedTransform = transforms.find(t => t.id === id)
          return selectedTransform.category !== transform.category || transform.category === 'neutral'
        })
        onTransformSelect([...filtered, transformId])
      } else {
        // Add to selection
        onTransformSelect([...selectedTransforms, transformId])
      }
    }
  }

  const isDisabled = (transformId) => {
    // Don't disable if already selected
    if (selectedTransforms.includes(transformId)) return false
    
    // Check if selecting this would conflict
    return hasConflict(transformId)
  }

  return (
    <div className="transform-container">
      {selectedTransforms.length > 0 && (
        <div className="selected-info">
          <span className="selected-count">
            {selectedTransforms.length} transformation{selectedTransforms.length !== 1 ? 's' : ''} selected
          </span>
          <button 
            className="clear-all-btn"
            onClick={() => onTransformSelect([])}
          >
            Clear All
          </button>
        </div>
      )}
      
      <div className="transform-buttons-grid">
        {transforms.map((transform) => {
          const isSelected = selectedTransforms.includes(transform.id)
          const disabled = isDisabled(transform.id)
          
          return (
            <button
              key={transform.id}
              onClick={() => handleTransformClick(transform.id)}
              disabled={disabled}
              className={`transform-button ${isSelected ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
              title={disabled ? 'Conflicts with current selection' : transform.label}
            >
              <span className="transform-icon">{transform.icon}</span>
              <span className="transform-label">{transform.label}</span>
              {isSelected && (
                <span className="selection-badge">
                  {selectedTransforms.indexOf(transform.id) + 1}
                </span>
              )}
            </button>
          )
        })}
      </div>
      
      {selectedTransforms.length > 1 && (
        <div className="transform-order-info">
          <span className="info-icon">ℹ️</span>
          <span>Transformations will be applied in order: {
            selectedTransforms.map((id, idx) => {
              const t = transforms.find(tr => tr.id === id)
              return idx === selectedTransforms.length - 1 ? t.label : `${t.label} → `
            }).join('')
          }</span>
        </div>
      )}
    </div>
  )
}

export default TransformButtons