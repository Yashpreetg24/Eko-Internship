import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { User, Briefcase, Calendar, Mail, CheckCircle2, Circle, Laptop, Shield, MessageSquare, Loader } from 'lucide-react';

const EmployeeProfile = () => {
  const { id } = useParams();
  const [employee, setEmployee] = useState(null);
  const [checklist, setChecklist] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const [empRes, checkRes, logsRes] = await Promise.all([
          fetch(`http://localhost:8000/employees/${id}`),
          fetch(`http://localhost:8000/employees/${id}/checklist`),
          fetch(`http://localhost:8000/employees/${id}/logs`)
        ]);
        
        if (empRes.ok) setEmployee(await empRes.json());
        if (checkRes.ok) setChecklist(await checkRes.json());
        if (logsRes.ok) setLogs(await logsRes.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    if (id) fetchEmployee();
  }, [id]);

  if (loading) {
    return <div className="flex justify-center items-center h-full"><Loader className="animate-spin text-blue-500" size={32} /></div>;
  }

  if (!employee) {
    return <div className="p-8 text-red-500">Employee not found.</div>;
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        
        {/* Profile Header */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 flex flex-col md:flex-row gap-8 items-start md:items-center">
          <div className="w-24 h-24 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-3xl font-bold">
            {employee.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{employee.name}</h1>
                <p className="text-gray-500 text-lg">{employee.role}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${employee.status === 'active' ? 'bg-emerald-100 text-emerald-700' : employee.status === 'pending' ? 'bg-amber-100 text-amber-700' : 'bg-rose-100 text-rose-700'}`}>
                {employee.status.toUpperCase()}
              </span>
            </div>
            
            <div className="flex flex-wrap gap-6 mt-6">
              <div className="flex items-center gap-2 text-gray-600">
                <Briefcase size={18} />
                <span>{employee.department}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Mail size={18} />
                <span>{employee.email}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Calendar size={18} />
                <span>Joined {new Date(employee.joining_date).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Progress & Accounts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Onboarding Progress</h3>
            <div className="flex justify-between items-end mb-2">
              <span className="text-3xl font-bold text-blue-600">{employee.onboarding_progress}%</span>
              <span className="text-gray-500 text-sm">Completed</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-3">
              <div className="bg-blue-600 h-3 rounded-full transition-all" style={{ width: `${employee.onboarding_progress}%` }}></div>
            </div>
            
            <h3 className="text-lg font-bold text-gray-800 mt-8 mb-4">Checklist</h3>
            <div className="space-y-3">
              {checklist.map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    {item.completed ? <CheckCircle2 className="text-emerald-500" size={20} /> : <Circle className="text-gray-300" size={20} />}
                    <span className={`font-medium ${item.completed ? 'text-gray-900 line-through opacity-70' : 'text-gray-700'}`}>{item.task_name}</span>
                  </div>
                  <span className="text-xs text-gray-500">
                    {item.completed ? `Done ${new Date(item.completed_date).toLocaleDateString()}` : `Due ${new Date(item.due_date).toLocaleDateString()}`}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Provisioning</h3>
              <ul className="space-y-4">
                <li className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-gray-700">
                    <Laptop size={18} className="text-gray-400" /> Laptop
                  </div>
                  {employee.laptop_allocated ? <span className="text-emerald-500 text-sm font-medium">Allocated</span> : <span className="text-amber-500 text-sm font-medium">Pending</span>}
                </li>
                <li className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-gray-700">
                    <Mail size={18} className="text-gray-400" /> Email
                  </div>
                  {employee.email_created ? <span className="text-emerald-500 text-sm font-medium">Created</span> : <span className="text-amber-500 text-sm font-medium">Pending</span>}
                </li>
                <li className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-gray-700">
                    <MessageSquare size={18} className="text-gray-400" /> Slack
                  </div>
                  {employee.slack_access ? <span className="text-emerald-500 text-sm font-medium">Invited</span> : <span className="text-amber-500 text-sm font-medium">Pending</span>}
                </li>
                <li className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-gray-700">
                    <Shield size={18} className="text-gray-400" /> VPN
                  </div>
                  {employee.vpn_setup ? <span className="text-emerald-500 text-sm font-medium">Setup</span> : <span className="text-amber-500 text-sm font-medium">Pending</span>}
                </li>
              </ul>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Interaction Logs</h3>
              <div className="space-y-4 max-h-64 overflow-y-auto pr-2">
                {logs.length > 0 ? logs.map(log => (
                  <div key={log.id} className="text-sm">
                    <div className="flex justify-between mb-1">
                      <span className="font-medium text-gray-800">{log.action}</span>
                      <span className={`text-xs ${log.status === 'Resolved' || log.status === 'Success' ? 'text-emerald-500' : 'text-rose-500'}`}>{log.status}</span>
                    </div>
                    <div className="text-xs text-gray-400">{new Date(log.timestamp).toLocaleString()} • {log.confidence}% conf.</div>
                  </div>
                )) : <div className="text-sm text-gray-500">No interaction logs found.</div>}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default EmployeeProfile;
