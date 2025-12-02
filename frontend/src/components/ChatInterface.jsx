import React, { useRef } from 'react';
import Header from './Header';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import FileUpload from './FileUpload';
import { useChat } from '../hooks/useChat';
import { useFileUpload } from '../hooks/useFileUpload';

const ChatInterface = () => {
  const fileUploadRef = useRef(null);
  const { messages, loading, sendMessage, addSystemMessage } = useChat();

  const handleUploadSuccess = (response) => {
    addSystemMessage(`✓ File "${response.filename}" uploaded successfully and indexed.`);
  };

  const handleUploadError = (error) => {
    addSystemMessage(`✗ Upload failed: ${error.message}`, true);
  };

  const { uploading, uploadFile } = useFileUpload(
    handleUploadSuccess,
    handleUploadError
  );

  const handleFileSelect = async (file) => {
    try {
      await uploadFile(file);
    } catch (error) {
      console.error('Upload error:', error);
    }
  };

  const triggerFileUpload = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = (e) => {
      const file = e.target.files?.[0];
      if (file) handleFileSelect(file);
    };
    input.click();
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header onUploadClick={triggerFileUpload} uploading={uploading} />

      <div className="flex-1 overflow-y-auto px-6 py-4">
        <MessageList messages={messages} loading={loading} />
      </div>

      <MessageInput onSend={sendMessage} loading={loading} disabled={false} />

      <FileUpload
        ref={fileUploadRef}
        onFileSelect={handleFileSelect}
        uploading={uploading}
      />
    </div>
  );
};

export default ChatInterface