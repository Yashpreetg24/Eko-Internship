import React, { useState } from 'react';
import { Send, CheckCircle2, Circle, AlertCircle, Terminal, BookOpen, Loader } from 'lucide-react';

const ChatPortal = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [isIdentified, setIsIdentified] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleIdentify = (e) => {
    e.preventDefault();
    if (employeeId.trim()) {
      setIsIdentified(true);
      setMessages([{
        sender: 'ai',
        text: `Hi ${employeeId} 👋 How can I help you with your onboarding today?`,
        type: 'greeting'
      }]);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employee_id: employeeId, message: userMessage.text })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: data.response,
        workflow_trace: data.workflow_trace,
        checklist: data.checklist,
        progress: data.progress,
        sources: data.sources,
        confidence: data.confidence,
        escalated: data.escalated
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Error connecting to the agent. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  if (!isIdentified) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 max-w-md w-full">
          <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Welcome to EmployeeClaw</h2>
          <form onSubmit={handleIdentify}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Enter your Employee ID</label>
              <input
                type="text"
                placeholder="e.g. EMP1001"
                className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-shadow"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
              />
            </div>
            <button type="submit" className="w-full bg-blue-600 text-white font-medium py-3 rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
              Start Chat
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white relative">
      <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl w-full flex gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-emerald-500 text-white'}`}>
                {msg.sender === 'user' ? 'U' : 'AI'}
              </div>
              <div className={`space-y-4 ${msg.sender === 'user' ? 'items-end flex flex-col' : 'items-start'}`}>
                <div className={`p-4 rounded-2xl ${msg.sender === 'user' ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-50 border border-gray-100 text-gray-800'}`}>
                  {msg.text}
                </div>
                
                {msg.sender === 'ai' && !msg.type && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                    {/* Workflow Trace */}
                    {msg.workflow_trace && msg.workflow_trace.length > 0 && (
                      <div className="bg-slate-900 text-slate-300 p-4 rounded-xl text-sm font-mono shadow-sm">
                        <div className="flex items-center gap-2 mb-3 text-slate-100 font-semibold border-b border-slate-700 pb-2">
                          <Terminal size={16} /> Workflow Trace
                        </div>
                        <ul className="space-y-1">
                          {msg.workflow_trace.map((step, i) => (
                            <li key={i} className="flex gap-2">
                              <span className={step.startsWith('✓') ? 'text-emerald-400' : 'text-rose-400'}>{step.charAt(0)}</span>
                              <span>{step.substring(1).trim()}</span>
                            </li>
                          ))}
                        </ul>
                        <div className="mt-3 pt-2 border-t border-slate-700 flex justify-between items-center text-xs">
                          <span>Confidence: <span className={msg.confidence >= 70 ? 'text-emerald-400' : 'text-rose-400'}>{msg.confidence}%</span></span>
                          {msg.escalated && <span className="text-rose-400 bg-rose-400/10 px-2 py-0.5 rounded">ESCALATED</span>}
                        </div>
                      </div>
                    )}

                    <div className="space-y-4">
                      {/* Onboarding Checklist */}
                      {msg.checklist && msg.checklist.length > 0 && (
                        <div className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
                          <div className="flex justify-between items-center mb-3">
                            <h3 className="font-semibold text-gray-800 text-sm">Onboarding Checklist</h3>
                            <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">{msg.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-100 rounded-full h-1.5 mb-4">
                            <div className="bg-blue-500 h-1.5 rounded-full transition-all" style={{ width: `${msg.progress}%` }}></div>
                          </div>
                          <ul className="space-y-2">
                            {msg.checklist.slice(0, 4).map((task, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                                {task.completed ? <CheckCircle2 size={16} className="text-emerald-500 mt-0.5 shrink-0" /> : <Circle size={16} className="text-gray-300 mt-0.5 shrink-0" />}
                                <span>{task.task_name}</span>
                              </li>
                            ))}
                            {msg.checklist.length > 4 && <li className="text-xs text-gray-400 pl-6">+{msg.checklist.length - 4} more tasks...</li>}
                          </ul>
                        </div>
                      )}

                      {/* Sources */}
                      {msg.sources && msg.sources.length > 0 && (
                        <div className="bg-blue-50/50 border border-blue-100 p-4 rounded-xl">
                          <div className="flex items-center gap-2 mb-2 text-blue-800 font-semibold text-sm">
                            <BookOpen size={16} /> Knowledge Sources
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {msg.sources.map((source, i) => (
                              <span key={i} className="text-xs bg-white border border-blue-200 text-blue-600 px-2 py-1 rounded shadow-sm">{source}</span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-50 border border-gray-100 p-4 rounded-2xl flex gap-2 items-center text-gray-500 shadow-sm ml-12">
              <Loader className="animate-spin" size={16} /> Agent is thinking...
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-white border-t border-gray-100">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto relative">
          <input
            type="text"
            className="w-full bg-gray-50 border border-gray-200 rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all shadow-sm"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={!input.trim() || loading}
            className="absolute right-2 top-2 bottom-2 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full w-10 h-10 flex items-center justify-center transition-colors disabled:opacity-50"
          >
            <Send size={18} className="ml-1" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPortal;
