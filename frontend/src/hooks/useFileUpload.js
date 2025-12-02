import { useState, useCallback } from 'react';
import apiService from '../services/api';

export const useFileUpload = (onSuccess, onError) => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const uploadFile = useCallback(
    async (file) => {
      try {
        if (!file) {
          throw new Error('No file selected');
        }

        setUploading(true);
        setProgress(0);

        // Simulate progress for better UX
        const progressInterval = setInterval(() => {
          setProgress((prev) => Math.min(prev + 10, 90));
        }, 200);

        const response = await apiService.uploadDocument(file);

        clearInterval(progressInterval);
        setProgress(100);

        setTimeout(() => {
          setProgress(0);
          setUploading(false);
          if (onSuccess) {
            onSuccess(response);
          }
        }, 500);
      } catch (err) {
        setUploading(false);
        setProgress(0);
        if (onError) {
          onError(err);
        }
        throw err;
      }
    },
    [onSuccess, onError]
  );

  return {
    uploading,
    progress,
    uploadFile,
  };
};