import React, { useState } from 'react'
import { saveHistoryItem } from '../utils/api'

const ResultDisplay = ({ text, onReset, transformType, historyId }) => {
  const [copied, setCopied] = useState(false)
  const [saved, setSaved] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text:', err)
    }
  }

  const handleSave = async () => {
    if (!historyId || saved || saving) return
    
    setSaving(true)
    try {
      const result = await saveHistoryItem(historyId)
      
      if (result.success) {
        setSaved(true)
        // Optional: Show a temporary success message
        setTimeout(() => {
          // Keep it saved, don't reset
        }, 2000)
      } else {
        console.error('Failed to save:', result.message)
        alert('Failed to save. Please try again.')
      }
    } catch (error) {
      console.error('Save error:', error)
      alert('Failed to save. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const getTransformLabel = (type) => {
    const labels = {
      grammar: 'Grammar Fixed',
      formal: 'Formal Tone',
      friendly: 'Friendly Tone',
      shorten: 'Shortened',
      expand: 'Expanded',
      bullet: 'Bullet Points',
      emoji: 'With Emojis',
      tweetify: 'Tweet Ready'
    }
    return labels[type] || 'Transformed'
  }

  return (
    <div className="result-container">
      <div className="result-header">
        <h3 className="result-title">
          {getTransformLabel(transformType)}
        </h3>
        <button
          onClick={onReset}
          className="reset-button"
        >
          ↻ Reset
        </button>
      </div>
      
      <div className="result-text-container">
        <div className="result-text-box">
          <p className="result-text">
            {text}
          </p>
        </div>
        
        <button
          onClick={handleCopy}
          className={`copy-icon-button ${copied ? 'copied' : ''}`}
          title={copied ? 'Copied!' : 'Copy to clipboard'}
        >
          {copied ? (
            <svg className="copy-icon" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="copy-icon" viewBox="0 0 20 20">
              <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
              <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
            </svg>
          )}
        </button>
      </div>
      
      <div className="result-actions">
        <button
          onClick={handleCopy}
          className="action-button copy-action-button"
        >
          <svg className="action-icon" viewBox="0 0 20 20">
            <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
            <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
          </svg>
          Copy
        </button>
        
        <button
          onClick={handleSave}
          className={`action-button save-action-button ${saved ? 'saved' : ''}`}
          disabled={saving || saved || !historyId}
          title={saved ? 'Saved!' : 'Save transformation'}
        >
          {saving ? (
            <>
              <svg className="action-icon animate-spin" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
              </svg>
              Saving...
            </>
          ) : saved ? (
            <>
              <span style={{ fontSize: '16px' }}>⭐</span>
              Saved
            </>
          ) : (
            <>
              <span style={{ fontSize: '16px' }}>⭐</span>
              Save
            </>
          )}
        </button>
      </div>
    </div>
  )
}

export default ResultDisplay