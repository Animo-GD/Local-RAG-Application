import React, { useState } from 'react';
import ChatInterface from "./components/ChatInterface";

const App = () => {
    const [config, setConfig] = useState({
        model: 'llama3.1:8b',
        selectedFiles: [] 
    });

    return <ChatInterface config={config} setConfig={setConfig} />;
}

export default App;