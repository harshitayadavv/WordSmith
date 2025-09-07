// frontend/src/utils/api.js
// API configuration for WordSmith backend

export const API_BASE_URL = 'http://127.0.0.1:8000';

// Test API connection function
export const testConnection = async () => {
  try {
    // Fixed: Correct health check endpoint
    const response = await fetch(`${API_BASE_URL}/api/v1/health`);
    const data = await response.json();
    console.log('Backend connection:', data);
    // Backend returns "healthy" or "unhealthy" - both indicate connection works
    return response.ok;
  } catch (error) {
    console.error('Backend connection failed:', error);
    return false;
  }
};

// Map frontend transform IDs to backend transformation types
const transformMapping = {
  'grammar': 'grammar_fix',
  'formal': 'formal',
  'friendly': 'friendly', 
  'shorten': 'shorten',
  'expand': 'expand',
  'bullet': 'bullet',
  'emoji': 'emoji',
  'tweetify': 'tweetify'
};

// Transform text function that calls your backend
export const transformText = async (text, transformType) => {
  try {
    // Map frontend transform ID to backend format
    const backendTransformType = transformMapping[transformType];
    
    if (!backendTransformType) {
      throw new Error(`Unknown transformation type: ${transformType}`);
    }

    // Fixed: Correct API endpoint and request format
    const response = await fetch(`${API_BASE_URL}/api/v1/transform`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        transformation_type: backendTransformType,
        additional_instructions: null
      })
    });
        
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }
        
    const data = await response.json();
    
    // Return in format expected by frontend
    return {
      success: true,
      transformedText: data.transformed_text,
      transformationType: data.transformation_type,
      processingTime: data.processing_time_seconds
    };
  } catch (error) {
    console.error('Transform request failed:', error);
    return {
      success: false,
      message: error.message || 'Transformation failed'
    };
  }
};

// Get available transformations
export const getAvailableTransformations = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/transformations`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to get transformations:', error);
    throw error;
  }
};