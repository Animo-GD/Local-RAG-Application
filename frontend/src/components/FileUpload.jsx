import React, { useRef } from 'react';

const FileUpload = ({ onFileSelect, uploading }) => {
  const fileInputRef = useRef(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleChange = (e) => {
    const file = e.target.files?.[0];
    if (file && onFileSelect) {
      onFileSelect(file);
    }
    // Reset input
    e.target.value = '';
  };

  return (
    <input
      ref={fileInputRef}
      type="file"
      className="hidden"
      onChange={handleChange}
      disabled={uploading}
    />
  );
};

export default FileUpload;