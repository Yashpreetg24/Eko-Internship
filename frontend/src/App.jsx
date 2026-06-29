import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatPortal from './pages/ChatPortal';
import HRDashboard from './pages/HRDashboard';
import EscalationDashboard from './pages/EscalationDashboard';
import EmployeeProfile from './pages/EmployeeProfile';

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50 font-sans">
        <Sidebar />
        <div className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<ChatPortal />} />
            <Route path="/dashboard" element={<HRDashboard />} />
            <Route path="/escalations" element={<EscalationDashboard />} />
            <Route path="/employee/:id" element={<EmployeeProfile />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
