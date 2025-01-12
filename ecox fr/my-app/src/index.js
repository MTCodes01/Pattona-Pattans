import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/global.css'; // Import global styles
import App from './App'; // Import the main App component

// Create the root of the React application
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
