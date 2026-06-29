import React, { useState, useEffect } from 'react';
import { Filter, CheckCircle, Loader } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const EscalationDashboard = () => {
  const [escalations, setEscalations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterTeam, setFilterTeam] = useState('All');
  const [filterStatus, setFilterStatus] = useState('All');

  useEffect(() => {
    fetchEscalations();
  }, []);

  const fetchEscalations = async () => {
    try {
      const res = await fetch(`${API_URL}/escalations`);
      const data = await res.json();
      setEscalations(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (id) => {
    try {
      await fetch(`${API_URL}/escalations/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'resolved' })
      });
      fetchEscalations();
    } catch (err) {
      console.error(err);
    }
  };

  const filteredEscalations = escalations.filter(esc => {
    if (filterTeam !== 'All' && esc.assigned_team !== filterTeam) return false;
    if (filterStatus !== 'All' && esc.status !== filterStatus.toLowerCase()) return false;
    return true;
  });

  if (loading) {
    return <div className="flex justify-center items-center h-full"><Loader className="animate-spin text-blue-500" size={32} /></div>;
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Escalations</h1>
          <p className="text-gray-500 mt-1">Manage and resolve employee issues</p>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 bg-white px-3 py-2 rounded-lg border border-gray-200 shadow-sm text-sm">
            <Filter size={16} className="text-gray-400" />
            <select className="bg-transparent outline-none text-gray-700" value={filterTeam} onChange={(e) => setFilterTeam(e.target.value)}>
              <option value="All">All Teams</option>
              <option value="HR">HR</option>
              <option value="IT">IT</option>
              <option value="Finance">Finance</option>
              <option value="Payroll">Payroll</option>
            </select>
          </div>
          <div className="flex items-center gap-2 bg-white px-3 py-2 rounded-lg border border-gray-200 shadow-sm text-sm">
            <Filter size={16} className="text-gray-400" />
            <select className="bg-transparent outline-none text-gray-700" value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
              <option value="All">All Statuses</option>
              <option value="Open">Open</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 text-gray-500 text-sm">
              <th className="p-4 font-medium">Employee</th>
              <th className="p-4 font-medium">Reason</th>
              <th className="p-4 font-medium">Priority</th>
              <th className="p-4 font-medium">Team</th>
              <th className="p-4 font-medium">Status</th>
              <th className="p-4 font-medium">Created At</th>
              <th className="p-4 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredEscalations.map((esc) => (
              <tr key={esc.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                <td className="p-4 text-sm font-medium text-gray-800">{esc.employee_id}</td>
                <td className="p-4 text-sm text-gray-600">{esc.reason}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                    esc.priority === 'high' ? 'bg-rose-100 text-rose-700' :
                    esc.priority === 'medium' ? 'bg-amber-100 text-amber-700' :
                    'bg-emerald-100 text-emerald-700'
                  }`}>
                    {esc.priority.toUpperCase()}
                  </span>
                </td>
                <td className="p-4 text-sm text-gray-600">{esc.assigned_team}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 text-xs rounded-full font-medium ${esc.status === 'open' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}`}>
                    {esc.status.toUpperCase()}
                  </span>
                </td>
                <td className="p-4 text-sm text-gray-500">{new Date(esc.created_at).toLocaleDateString()}</td>
                <td className="p-4">
                  {esc.status === 'open' ? (
                    <button onClick={() => handleResolve(esc.id)} className="flex items-center gap-1 text-sm text-emerald-600 hover:text-emerald-700 font-medium">
                      <CheckCircle size={16} /> Resolve
                    </button>
                  ) : (
                    <span className="text-gray-400 text-sm">Resolved</span>
                  )}
                </td>
              </tr>
            ))}
            {filteredEscalations.length === 0 && (
              <tr>
                <td colSpan="7" className="p-8 text-center text-gray-500">No escalations found matching filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EscalationDashboard;
