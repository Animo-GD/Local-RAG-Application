import React, { useRef, useEffect } from 'react';
import { Database, FileText, AlertCircle, CheckCircle, Bot, User } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import { MESSAGE_ROLES } from '../utils/constant.js';

const MessageList = ({ messages, loading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'sql':
        return <Database className="w-4 h-4" />;
      case 'document':
        return <FileText className="w-4 h-4" />;
      default:
        return null;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'sql':
        return 'text-purple-400';
      case 'document':
        return 'text-green-400';
      default:
        return 'text-slate-400';
    }
  };

  if (messages.length === 0 && !loading) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400">
        <Database className="w-16 h-16 mb-4 opacity-50" />
        <h2 className="text-xl font-semibold mb-2">Welcome to RAG System</h2>
        <p className="text-center max-w-md mb-4">
          Ask questions about your documents or databases. Upload documents to get started.
        </p>
        <div className="flex gap-2 flex-wrap justify-center max-w-lg">
          <span className="px-3 py-1 bg-slate-800 rounded-full text-sm">
            "What is in the documents?"
          </span>
          <span className="px-3 py-1 bg-slate-800 rounded-full text-sm">
            "Query the database"
          </span>
          <span className="px-3 py-1 bg-slate-800 rounded-full text-sm">
            "Summarize the content"
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${
            msg.role === MESSAGE_ROLES.USER ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`flex gap-3 max-w-3xl ${
              msg.role === MESSAGE_ROLES.USER ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            {/* Avatar */}
            <div
              className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                msg.role === MESSAGE_ROLES.USER
                  ? 'bg-blue-600'
                  : msg.role === MESSAGE_ROLES.SYSTEM
                  ? 'bg-slate-700'
                  : 'bg-slate-800 border border-slate-700'
              }`}
            >
              {msg.role === MESSAGE_ROLES.USER ? (
                <User className="w-5 h-5 text-white" />
              ) : msg.role === MESSAGE_ROLES.SYSTEM ? (
                msg.error ? (
                  <AlertCircle className="w-5 h-5 text-red-400" />
                ) : (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                )
              ) : (
                <Bot className="w-5 h-5 text-slate-400" />
              )}
            </div>

            {/* Message Content */}
            <div
              className={`rounded-2xl px-4 py-3 ${
                msg.role === MESSAGE_ROLES.USER
                  ? 'bg-blue-600 text-white'
                  : msg.role === MESSAGE_ROLES.SYSTEM
                  ? msg.error
                    ? 'bg-red-900/30 text-red-200 border border-red-800'
                    : 'bg-green-900/30 text-green-200 border border-green-800'
                  : msg.error
                  ? 'bg-red-900/30 text-red-200 border border-red-800'
                  : 'bg-slate-800 text-slate-100 border border-slate-700'
              }`}
            >
              {/* Query Type Badge */}
              {msg.role === MESSAGE_ROLES.ASSISTANT && msg.queryType && !msg.error && (
                <div
                  className={`flex items-center gap-2 mb-2 text-xs ${getTypeColor(
                    msg.queryType
                  )}`}
                >
                  {getTypeIcon(msg.queryType)}
                  <span className="capitalize">{msg.queryType} Query</span>
                </div>
              )}

              {/* Message Text */}
              <p className="whitespace-pre-wrap break-words">{msg.content}</p>

              {/* SQL Query Display */}
              {msg.sqlQuery && (
                <div className="mt-3 p-3 bg-slate-900/50 rounded-lg">
                  <div className="text-xs text-slate-400 mb-1 font-semibold">
                    SQL Query:
                  </div>
                  <pre className="text-xs font-mono text-slate-300 overflow-x-auto">
                    {msg.sqlQuery}
                  </pre>
                </div>
              )}

              {/* Metadata */}
              {msg.metadata && Object.keys(msg.metadata).length > 0 && (
                <div className="mt-2 text-xs text-slate-400">
                  {msg.metadata.retrieved_docs && (
                    <span>📄 {msg.metadata.retrieved_docs} documents retrieved</span>
                  )}
                </div>
              )}

              {/* Error Icon */}
              {msg.error && (
                <div className="flex items-center gap-2 mt-2 text-xs">
                  <AlertCircle className="w-4 h-4" />
                  <span>Error occurred</span>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}

      {loading && (
        <div className="flex justify-start">
          <div className="flex gap-3 max-w-3xl">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
              <Bot className="w-5 h-5 text-slate-400" />
            </div>
            <div className="bg-slate-800 border border-slate-700 rounded-2xl px-4 py-3">
              <LoadingSpinner size="sm" text="Thinking..." />
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;