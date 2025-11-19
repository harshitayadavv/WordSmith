import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import Navigation from './components/Navigation'
import TextInput from './components/TextInput'
import TransformButtons from './components/TransformButtons'
import ConvertButton from './components/ConvertButton'
import ResultDisplay from './components/ResultDisplay'
import LoadingSpinner from './components/LoadingSpinner'
import History from './components/History'
import SavedChats from './components/SavedChats'
import { transformText, testConnection } from './utils/api'

function App() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [selectedTransforms, setSelectedTransforms] = useState([]) // CHANGED: Array instead of string
  const [isLoading, setIsLoading] = useState(false)
  const [showResult, setShowResult] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')
  const [activeTab, setActiveTab] = useState('chat')
  const [currentHistoryId, setCurrentHistoryId] = useState(null)

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
    // Recheck every 10 seconds if disconnected
    const interval = setInterval(() => {
      if (backendStatus !== 'connected') {
        checkBackend()
      }
    }, 10000)
    
    return () => clearInterval(interval)
  }, [backendStatus])

  const handleTransform = async () => {
    if (!inputText.trim() || selectedTransforms.length === 0) {
      return
    }

    setIsLoading(true)
    setShowResult(false)

    try {
      // Apply transformations sequentially
      let currentText = inputText
      let lastHistoryId = null
      
      for (let i = 0; i < selectedTransforms.length; i++) {
        const transformType = selectedTransforms[i]
        
        const result = await transformText(currentText, transformType)
        
        if (result.success) {
          currentText = result.transformedText
          lastHistoryId = result.historyId
        } else {
          throw new Error(result.message || `Transformation ${i + 1} failed`)
        }
      }
      
      setOutputText(currentText)
      setCurrentHistoryId(lastHistoryId)
      setShowResult(true)
      
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
    setSelectedTransforms([])
    setShowResult(false)
    setCurrentHistoryId(null)
  }

  const handleUseHistory = (historyItem) => {
    setInputText(historyItem.original_text)
    setOutputText(historyItem.transformed_text)
    setCurrentHistoryId(historyItem.id)
    
    // Map backend transformation type to frontend format
    const typeMap = {
      'grammar_fix': 'grammar',
      'formal': 'formal',
      'friendly': 'friendly',
      'shorten': 'shorten',
      'expand': 'expand',
      'bullet': 'bullet',
      'emoji': 'emoji',
      'tweetify': 'tweetify'
    }
    
    const mappedType = typeMap[historyItem.transformation_type] || historyItem.transformation_type
    setSelectedTransforms([mappedType]) // Set as array with single item
    setShowResult(true)
    setActiveTab('chat')
  }

  const handleTabChange = (tab) => {
    setActiveTab(tab)
    if (tab === 'chat') {
      setShowResult(false)
    }
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
        
        {/* Navigation Tabs */}
        <Navigation activeTab={activeTab} onTabChange={handleTabChange} />
        
        <div className="main-content">
          <div className="content-space">
            {/* Chat Tab */}
            {activeTab === 'chat' && (
              <>
                {!showResult ? (
                  <>
                    <TextInput 
                      value={inputText}
                      onChange={setInputText}
                      placeholder="Paste your text here..."
                    />
                    
                    <TransformButtons 
                      selectedTransforms={selectedTransforms}
                      onTransformSelect={setSelectedTransforms}
                    />
                    
                    <ConvertButton 
                      onClick={handleTransform}
                      disabled={!inputText.trim() || selectedTransforms.length === 0 || isLoading || backendStatus !== 'connected'}
                      isLoading={isLoading}
                    />
                  </>
                ) : (
                  <ResultDisplay 
                    text={outputText}
                    onReset={handleReset}
                    transformType={selectedTransforms[selectedTransforms.length - 1]} // Show last transform
                    historyId={currentHistoryId}
                  />
                )}
              </>
            )}
            
            {/* History Tab */}
            {activeTab === 'history' && (
              <div className="tab-content">
                <History
                  onClose={() => setActiveTab('chat')}
                  onUseHistory={handleUseHistory}
                  embedded={true}
                />
              </div>
            )}
            
            {/* Saved Tab */}
            {activeTab === 'saved' && (
              <div className="tab-content">
                <SavedChats onUseHistory={handleUseHistory} />
              </div>
            )}
          </div>
        </div>
        
        {isLoading && <LoadingSpinner />}
      </div>
    </div>
  )
}

export default App