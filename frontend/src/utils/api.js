// frontend/src/utils/api.js
export const API_BASE_URL = 'https://wordsmith-backend-iatg.onrender.com';

const getUserId = () => {
  let userId = localStorage.getItem('wordsmith_user_id');
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('wordsmith_user_id', userId);
  }
  return userId;
};

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

export const transformText = async (text, transformType, originalText = null) => {
  console.log('=== TRANSFORM START ===');
  console.log('Input text:', text);
  console.log('Original text:', originalText);
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
      user_id: getUserId(),
      original_text: originalText
    };
    
    console.log('Request body:', requestBody);

    const response = await fetch(`${API_BASE_URL}/api/v1/transform`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }
        
    const data = await response.json();
    console.log('Success response:', data);
    
    return {
      success: true,
      transformedText: data.transformed_text,
      transformationType: data.transformation_type,
      processingTime: data.processing_time,
      historyId: data.history_id
    };
  } catch (error) {
    console.error('Transform request failed:', error);
    return {
      success: false,
      message: error.message || 'Transformation failed'
    };
  }
};

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

export const getHistory = async (page = 1, pageSize = 20, filters = {}) => {
  try {
    const userId = getUserId();
    const params = new URLSearchParams({
      user_id: userId,
      page: page.toString(),
      page_size: pageSize.toString(),
      ...filters
    });

    const response = await fetch(`${API_BASE_URL}/api/v1/history?${params}`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return { success: true, ...data };
  } catch (error) {
    console.error('Get history failed:', error);
    return { success: false, message: error.message || 'Failed to fetch history' };
  }
};

export const saveHistoryItem = async (historyId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/history/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ history_id: historyId })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return { success: true, ...data };
  } catch (error) {
    console.error('Save history item failed:', error);
    return { success: false, message: error.message || 'Failed to save item' };
  }
};

export const deleteHistoryItems = async (historyIds) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/history`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ history_ids: historyIds })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return { success: true, ...data };
  } catch (error) {
    console.error('Delete history items failed:', error);
    return { success: false, message: error.message || 'Failed to delete items' };
  }
};