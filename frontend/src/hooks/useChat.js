import { useState, useCallback } from 'react';
import apiService from '../services/api.js';
import { MESSAGE_ROLES } from '../utils/constant.js';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (question, config = {}) => {
    if (!question.trim()) return;

    const userMessage = {
      role: MESSAGE_ROLES.USER,
      content: question,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.query(question, config);

      const assistantMessage = {
        role: MESSAGE_ROLES.ASSISTANT,
        content: response.answer,
        queryType: response.query_type,
        sqlQuery: response.sql_query,
        context: response.context,
        metadata: response.metadata,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = {
        role: MESSAGE_ROLES.ASSISTANT,
        content: err.message || 'An error occurred while processing your request.',
        error: true,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const addSystemMessage = useCallback((content, isError = false) => {
    const systemMessage = {
      role: MESSAGE_ROLES.SYSTEM,
      content,
      error: isError,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, systemMessage]);
  }, []);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
    addSystemMessage,
  };
};