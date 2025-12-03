import React, { useState, useEffect } from 'react';
import { Database, Github, Settings, Moon, Sun, Trash2, FileText, Server } from 'lucide-react';
import api from '../services/api';

const Header = ({ onUploadClick, uploading, config, setConfig }) => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    if (isSettingsOpen) {
      loadDocuments();
    }
  }, [isSettingsOpen]);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const loadDocuments = async () => {
    try {
      const res = await api.listDocuments();
      setDocuments(res.documents);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (filename) => {
    if (confirm(`Are you sure you want to delete ${filename}?`)) {
      try {
        await api.deleteDocument(filename);
        loadDocuments();
        setConfig(prev => ({
            ...prev,
            selectedFiles: prev.selectedFiles.filter(f => f !== filename)
        }));
      } catch (e) {
        alert("Failed to delete file");
      }
    }
  };

  const toggleFileSelection = (filename) => {
    setConfig(prev => {
        const isSelected = prev.selectedFiles.includes(filename);
        return {
            ...prev,
            selectedFiles: isSelected 
                ? prev.selectedFiles.filter(f => f !== filename)
                : [...prev.selectedFiles, filename]
        };
    });
  };

  return (
    <div className="bg-white dark:bg-slate-800/50 backdrop-blur-sm border-b border-gray-200 dark:border-slate-700 px-6 py-4 transition-colors duration-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-lg">
            <Database className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800 dark:text-blue-500">RAG System</h1>
            <p className="text-sm text-gray-500 dark:text-slate-400">
              Local Knowledge Base
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
            <button 
                onClick={() => setDarkMode(!darkMode)} 
                className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-slate-700 text-gray-600 dark:text-slate-300 transition-colors"
            >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            <button 
                onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                className={`p-2 rounded-full hover:bg-gray-200 dark:hover:bg-slate-700 transition-colors ${isSettingsOpen ? 'bg-gray-200 dark:bg-slate-700 text-blue-600' : 'text-gray-600 dark:text-slate-300'}`}
                title="Configuration"
            >
                <Settings className="w-5 h-5" />
            </button>
            
             <button
            onClick={onUploadClick}
            disabled={uploading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
          >
            {uploading ? (
                 <span className="text-sm font-medium">Uploading...</span>
            ) : (
                <span className="text-sm font-medium">Upload Document</span>
            )}
          </button>

           <a href="https://github.com/Animo-GD/Local-RAG-Application" target="_blank" rel="noopener noreferrer" className="p-2 text-gray-500 dark:text-slate-400 hover:text-black dark:hover:text-white transition-colors">
            <Github className="w-5 h-5" />
          </a>
        </div>
      </div>

      {/* Settings Panel */}
      {isSettingsOpen && (
        <div className="mt-4 p-4 bg-gray-50 dark:bg-slate-900 rounded-lg border border-gray-200 dark:border-slate-700 shadow-lg text-gray-800 dark:text-slate-200 animate-in fade-in slide-in-from-top-2 duration-200">
            <h3 className="font-bold mb-3 border-b border-gray-300 dark:border-slate-700 pb-2 flex items-center gap-2">
                <Settings className="w-4 h-4" /> Local Configuration
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Model Settings */}
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300 flex items-center gap-2">
                             <Server className="w-4 h-4" /> Ollama Model
                        </label>
                        <input 
                            type="text" 
                            value={config.model}
                            onChange={(e) => setConfig({...config, model: e.target.value})}
                            placeholder="llama3.1:8b"
                            className="w-full p-2 rounded bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            Ensure this model is pulled in your local Ollama instance (e.g., <code>ollama pull llama3.1</code>).
                        </p>
                    </div>
                </div>

                {/* Knowledge Base Selection */}
                <div>
                    <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        Select Documents to Query
                    </label>
                    <div className="max-h-60 overflow-y-auto border border-gray-300 dark:border-slate-600 rounded bg-white dark:bg-slate-800 p-2 scrollbar-thin scrollbar-thumb-gray-400 dark:scrollbar-thumb-slate-600">
                        {documents.length === 0 ? (
                            <p className="text-sm text-gray-500 text-center py-2">No files uploaded</p>
                        ) : (
                            documents.map((doc, idx) => (
                                <div key={idx} className="flex items-center justify-between p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded transition-colors group">
                                    <div className="flex items-center gap-2 overflow-hidden flex-1 cursor-pointer" onClick={() => toggleFileSelection(doc)}>
                                        <input 
                                            type="checkbox"
                                            checked={config.selectedFiles.includes(doc)}
                                            onChange={() => {}} 
                                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                                        />
                                        <FileText className="w-4 h-4 text-blue-500 flex-shrink-0" />
                                        <span className="text-sm truncate select-none text-gray-700 dark:text-gray-200" title={doc}>{doc}</span>
                                    </div>
                                    <button 
                                        onClick={(e) => { e.stopPropagation(); handleDelete(doc); }}
                                        className="text-gray-400 hover:text-red-500 p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                                        title="Delete file"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            ))
                        )}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                        Select specific files to narrow down the search context. If none selected, all files are used.
                    </p>
                </div>
            </div>
        </div>
      )}
    </div>
  );
};

export default Header;