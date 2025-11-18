import React from 'react'

const ConvertButton = ({ onClick, disabled, isLoading }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="convert-button"
    >
      {isLoading ? (
        <div className="convert-button-loading">
          <div className="convert-button-spinner"></div>
          <span>Converting...</span>
        </div>
      ) : (
        'Convert'
      )}
    </button>
  )
}

export default ConvertButton