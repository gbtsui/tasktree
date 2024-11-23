import React from 'react'
import { ReactFlowProvider, Background } from '@xyflow/react';
import ReactDOM from 'react-dom/client'

import 'reactflow/dist/style.css';
import './index.css'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ReactFlowProvider>
      <Background />
      <div style={{ width: '100vw', height: '100vh' }}>
       <App />
      </div>
    </ReactFlowProvider>
  </React.StrictMode>,
)
