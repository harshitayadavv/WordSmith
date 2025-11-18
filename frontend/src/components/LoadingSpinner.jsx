import React from 'react'

const LoadingSpinner = () => {
  return (
    <div className="loading-overlay">
      <div className="loading-modal">
        <div className="loading-spinner-container">
          <div className="loading-spinner-bg"></div>
          <div className="loading-spinner"></div>
        </div>
        <p className="loading-text">Transforming text...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner