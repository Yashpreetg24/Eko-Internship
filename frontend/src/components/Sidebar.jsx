import React from 'react';
import { NavLink } from 'react-router-dom';
import { MessageSquare, LayoutDashboard, AlertTriangle, Users } from 'lucide-react';

const Sidebar = () => {
  return (
    <div className="w-64 bg-gray-900 text-white h-screen flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold tracking-wider text-blue-400">EmployeeClaw</h1>
        <p className="text-gray-400 text-sm mt-1">Autonomous Onboarding</p>
      </div>
      
      <nav className="flex-1 mt-6">
        <ul className="space-y-2 px-4">
          <li>
            <NavLink to="/" className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
              <MessageSquare size={20} />
              <span>Chat Portal</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/dashboard" className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
              <LayoutDashboard size={20} />
              <span>HR Dashboard</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/escalations" className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
              <AlertTriangle size={20} />
              <span>Escalations</span>
            </NavLink>
          </li>
          <li>
            {/* Using a placeholder for one employee for demo, could be an employee directory list */}
            <NavLink to="/employee/EMP1001" className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
              <Users size={20} />
              <span>My Profile</span>
            </NavLink>
          </li>
        </ul>
      </nav>
      
      <div className="p-6 text-xs text-gray-500">
        &copy; 2026 EmployeeClaw Inc.
      </div>
    </div>
  );
};

export default Sidebar;
