import React from 'react';
import ReactDOM from 'react-dom/client';  // Ensure you're importing from 'react-dom/client' (React 18)
import App from './App';  // Assuming your main app component is 'App.js'
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));  // Ensure this targets the correct div
root.render(<App />);
