import { API_BASE_URL } from '../utils/constants.js';

class APIService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async query(question) {
    try {
      const response = await fetch(`${this.baseURL}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process query');
      }

      return await response.json();
    } catch (error) {
      console.error('Query error:', error);
      throw error;
    }
  }

  async uploadDocument(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${this.baseURL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to upload document');
      }

      return await response.json();
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  }

  async checkHealth() {
    try {
      const response = await fetch(`${this.baseURL}/api/health`);
      if (!response.ok) throw new Error('Health check failed');
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  async listDocuments() {
    try {
      const response = await fetch(`${this.baseURL}/api/documents`);
      if (!response.ok) throw new Error('Failed to list documents');
      return await response.json();
    } catch (error) {
      console.error('List documents error:', error);
      throw error;
    }
  }
}

export default new APIService();