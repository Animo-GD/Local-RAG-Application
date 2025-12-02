export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const QUERY_TYPES = {
  DOCUMENT: 'document',
  SQL: 'sql',
  GENERAL: 'general'
};

export const MESSAGE_ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system'
};
