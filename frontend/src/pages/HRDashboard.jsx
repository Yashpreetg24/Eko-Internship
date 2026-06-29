import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, LineChart, Line, ResponsiveContainer } from 'recharts';
import { Users, CheckCircle, Clock, AlertTriangle, TrendingUp, Loader } from 'lucide-react';

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'];

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const HRDashboard = () => {
  const [data, setData] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [escalations, setEscalations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [analyticsRes, employeesRes, escalationsRes] = await Promise.all([
          fetch(`${API_URL}/analytics`),
          fetch(`${API_URL}/employees`),
          fetch(`${API_URL}/escalations`)
        ]);
        
        const analyticsData = await analyticsRes.json();
        const employeesData = await employeesRes.json();
        const escalationsData = await escalationsRes.json();
        
        setData(analyticsData);
        setEmployees(employeesData.slice(0, 5)); // Last 5
        setEscalations(escalationsData.slice(0, 5)); // Last 5
      } catch (err) {
        console.error("Failed to fetch dashboard data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-full"><Loader className="animate-spin text-blue-500" size={32} /></div>;
  }

  if (!data) return <div className="p-8 text-red-500">Failed to load dashboard. Make sure backend is running.</div>;

  const pieData = [
    { name: 'Completed', value: data.completed_onboarding },
    { name: 'Pending', value: data.pending_onboarding }
  ];

  const barData = Object.entries(data.escalations_by_team).map(([team, count]) => ({
    team, count
  }));

  return (
    <div className="h-full overflow-y-auto bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">HR Dashboard</h1>
          <p className="text-gray-500 mt-1">Overview of company onboarding status</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
        {[
          { title: 'Total Employees', value: data.total_employees, icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
          { title: 'Completed', value: data.completed_onboarding, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-100' },
          { title: 'Pending', value: data.pending_onboarding, icon: Clock, color: 'text-amber-600', bg: 'bg-amber-100' },
          { title: 'Escalated', value: data.escalated_cases, icon: AlertTriangle, color: 'text-rose-600', bg: 'bg-rose-100' },
          { title: 'Avg Completion', value: `${data.average_completion_percentage}%`, icon: TrendingUp, color: 'text-purple-600', bg: 'bg-purple-100' },
        ].map((stat, i) => (
          <div key={i} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center gap-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${stat.bg} ${stat.color}`}>
              <stat.icon size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">{stat.title}</p>
              <h3 className="text-2xl font-bold text-gray-800">{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Onboarding Status</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Escalations by Team</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="team" />
                <YAxis />
                <RechartsTooltip cursor={{fill: '#f3f4f6'}} />
                <Bar dataKey="count" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pb-8">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 className="text-lg font-bold text-gray-800">Recent Escalations</h3>
          </div>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 text-gray-500 text-sm">
                <th className="p-4 font-medium">Employee ID</th>
                <th className="p-4 font-medium">Team</th>
                <th className="p-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {escalations.map((esc) => (
                <tr key={esc.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50">
                  <td className="p-4 text-sm font-medium text-gray-800">{esc.employee_id}</td>
                  <td className="p-4 text-sm text-gray-600">{esc.assigned_team}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${esc.status === 'open' ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'}`}>
                      {esc.status.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 className="text-lg font-bold text-gray-800">Recently Active Employees</h3>
          </div>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 text-gray-500 text-sm">
                <th className="p-4 font-medium">Name</th>
                <th className="p-4 font-medium">Department</th>
                <th className="p-4 font-medium">Progress</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.employee_id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50">
                  <td className="p-4 text-sm font-medium text-gray-800">
                    <div>{emp.name}</div>
                    <div className="text-xs text-gray-500 font-normal">{emp.employee_id}</div>
                  </td>
                  <td className="p-4 text-sm text-gray-600">{emp.department}</td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-gray-100 rounded-full h-1.5 w-24">
                        <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${emp.onboarding_progress}%` }}></div>
                      </div>
                      <span className="text-xs font-medium text-gray-600">{emp.onboarding_progress}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default HRDashboard;
