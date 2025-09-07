import React from 'react'

const TransformButtons = ({ selectedTransform, onTransformSelect }) => {
  const transforms = [
    { id: 'grammar', label: 'Grammar Fix', icon: '✏️' },
    { id: 'formal', label: 'Formal', icon: '💼' },
    { id: 'friendly', label: 'Friendly', icon: '😊' },
    { id: 'shorten', label: 'Shorten', icon: '✓' },
    { id: 'expand', label: 'Expand', icon: '📈' },
    { id: 'bullet', label: 'Bullet', icon: '🔘' },
    { id: 'emoji', label: 'Emoji', icon: '😎' },
    { id: 'tweetify', label: 'Tweetify', icon: '🐦' },
  ]

  return (
    <div className="transform-buttons-grid">
      {transforms.map((transform) => (
        <button
          key={transform.id}
          onClick={() => onTransformSelect(transform.id)}
          className={`transform-button ${
            selectedTransform === transform.id ? 'active' : ''
          }`}
        >
          <span>{transform.icon}</span>
          <span>{transform.label}</span>
        </button>
      ))}
    </div>
  )
}

export default TransformButtons