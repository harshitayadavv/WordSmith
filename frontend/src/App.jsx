import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import TextInput from './components/TextInput'
import TransformButtons from './components/TransformButtons'
import ConvertButton from './components/ConvertButton'
import ResultDisplay from './components/ResultDisplay'
import LoadingSpinner from './components/LoadingSpinner'
import { transformText, testConnection } from './utils/api'

function App() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [selectedTransform, setSelectedTransform] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showResult, setShowResult] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')

  // Check backend connection on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const isConnected = await testConnection()
        setBackendStatus(isConnected ? 'connected' : 'disconnected')
      } catch (error) {
        console.error('Backend check failed:', error)
        setBackendStatus('disconnected')
      }
    }
    
    checkBackend()
  }, [])

  const handleTransform = async () => {
    if (!inputText.trim() || !selectedTransform) {
      return
    }

    setIsLoading(true)
    setShowResult(false)

    try {
      // Call the actual backend API
      const result = await transformText(inputText, selectedTransform)
      
      if (result.success) {
        setOutputText(result.transformedText)
        setShowResult(true)
      } else {
        throw new Error(result.message || 'Transformation failed')
      }
    } catch (error) {
      console.error('Transform error:', error)
      setOutputText(`Error: ${error.message || 'Sorry, there was an error processing your text. Please try again.'}`)
      setShowResult(true)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setInputText('')
    setOutputText('')
    setSelectedTransform('')
    setShowResult(false)
  }

  return (
    <div className="extension-container">
      <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Header />
        
        {/* Backend status indicator */}
        {backendStatus !== 'connected' && (
          <div className="backend-status" style={{
            padding: '8px 16px',
            backgroundColor: backendStatus === 'checking' ? '#fbbf24' : '#ef4444',
            color: 'white',
            fontSize: '12px',
            textAlign: 'center',
            fontWeight: '500'
          }}>
            {backendStatus === 'checking' ? '🔄 Checking backend connection...' : '❌ Backend not connected'}
          </div>
        )}
        
        <div className="main-content">
          <div className="content-space">
            {!showResult ? (
              <>
                <TextInput 
                  value={inputText}
                  onChange={setInputText}
                  placeholder="Paste your text here..."
                />
                
                <TransformButtons 
                  selectedTransform={selectedTransform}
                  onTransformSelect={setSelectedTransform}
                />
                
                <ConvertButton 
                  onClick={handleTransform}
                  disabled={!inputText.trim() || !selectedTransform || isLoading || backendStatus !== 'connected'}
                  isLoading={isLoading}
                />
              </>
            ) : (
              <ResultDisplay 
                text={outputText}
                onReset={handleReset}
                transformType={selectedTransform}
              />
            )}
          </div>
        </div>
        
        {isLoading && <LoadingSpinner />}
      </div>
    </div>
  )
}

export default App