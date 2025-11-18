import React from 'react'

const TextInput = ({ value, onChange, placeholder }) => {
  return (
    <div className="text-input-container">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="text-input"
      />
    </div>
  )
}

export default TextInput