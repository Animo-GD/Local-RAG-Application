import React, { useState, useRef, useEffect } from 'react';
import { Send, StopCircle } from 'lucide-react';

const MessageInput = ({ onSend, loading, disabled }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    if (!input.trim() || loading || disabled) return;
    onSend(input);
    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [input]);

  return (
    <div className="border-t border-slate-700 bg-slate-800/50 backdrop-blur-sm px-6 py-4">
      <div className="flex gap-3 max-w-4xl mx-auto">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about your documents or database..."
          className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[52px] max-h-[200px]"
          disabled={loading || disabled}
          rows={1}
        />
        <button
          onClick={handleSubmit}
          disabled={loading || !input.trim() || disabled}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-xl px-6 py-3 font-medium transition-colors flex items-center gap-2 self-end"
        >
          {loading ? (
            <>
              <StopCircle className="w-5 h-5" />
              <span className="hidden sm:inline">Stop</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span className="hidden sm:inline">Send</span>
            </>
          )}
        </button>
      </div>
      <div className="text-center text-xs text-slate-500 mt-2">
        Press Enter to send, Shift+Enter for new line
      </div>
    </div>
  );
};

export default MessageInput;