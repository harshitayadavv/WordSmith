// frontend/src/utils/api.js
// API configuration for WordSmith backend

export const API_BASE_URL = 'https://wordsmith-backend-iatg.onrender.com';

// Get or create user ID (stored in localStorage)
const getUserId = () => {
  let userId = localStorage.getItem('wordsmith_user_id');
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('wordsmith_user_id', userId);
  }
  console.log('User ID:', userId); // DEBUG
  return userId;
};

// Test API connection function
export const testConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/health`);
    const data = await response.json();
    console.log('Backend connection:', data);
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
  console.log('=== TRANSFORM START ===');
  console.log('Input text:', text);
  console.log('Transform type:', transformType);
  
  try {
    const backendTransformType = transformMapping[transformType];
    
    if (!backendTransformType) {
      throw new Error(`Unknown transformation type: ${transformType}`);
    }

    const requestBody = {
      text: text,
      transformation_type: backendTransformType,
      additional_instructions: null,
      user_id: getUserId()
    };
    
    console.log('Sending request to:', `${API_BASE_URL}/api/v1/transform`);
    console.log('Request body:', requestBody);

    const response = await fetch(`${API_BASE_URL}/api/v1/transform`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });
    
    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);
        
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error response:', errorData);
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }
        
    const data = await response.json();
    console.log('Success response:', data);
    console.log('History ID:', data.history_id);
    
    const result = {
      success: true,
      transformedText: data.transformed_text,
      transformationType: data.transformation_type,
      processingTime: data.processing_time,
      historyId: data.history_id
    };
    
    console.log('Returning result:', result);
    console.log('=== TRANSFORM END ===');
    
    return result;
  } catch (error) {
    console.error('Transform request failed:', error);
    console.log('=== TRANSFORM ERROR ===');
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

// ============= HISTORY API FUNCTIONS =============

// Get transformation history
export const getHistory = async (page = 1, pageSize = 20, filters = {}) => {
  console.log('=== GET HISTORY START ===');
  try {
    const userId = getUserId();
    const params = new URLSearchParams({
      user_id: userId,
      page: page.toString(),
      page_size: pageSize.toString(),
      ...filters
    });

    const url = `${API_BASE_URL}/api/v1/history?${params}`;
    console.log('Fetching history from:', url);

    const response = await fetch(url);
    
    console.log('History response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('History data:', data);
    console.log('Number of items:', data.items?.length);
    console.log('=== GET HISTORY END ===');
    
    return {
      success: true,
      ...data
    };
  } catch (error) {
    console.error('Get history failed:', error);
    console.log('=== GET HISTORY ERROR ===');
    return {
      success: false,
      message: error.message || 'Failed to fetch history'
    };
  }
};

// Save a history item (mark as permanent)
export const saveHistoryItem = async (historyId) => {
  console.log('Saving history item:', historyId);
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/history/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        history_id: historyId
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('Save response:', data);
    return {
      success: true,
      ...data
    };
  } catch (error) {
    console.error('Save history item failed:', error);
    return {
      success: false,
      message: error.message || 'Failed to save item'
    };
  }
};

// Delete history items
export const deleteHistoryItems = async (historyIds) => {
  console.log('Deleting history items:', historyIds);
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/history`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        history_ids: historyIds
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('Delete response:', data);
    return {
      success: true,
      ...data
    };
  } catch (error) {
    console.error('Delete history items failed:', error);
    return {
      success: false,
      message: error.message || 'Failed to delete items'
    };
  }
};