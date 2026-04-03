import React from 'react';
import { Database, LineChart, Cpu, History, LayoutDashboard } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'data', label: 'Dataset Management', icon: <Database size={20} /> },
    { id: 'models', label: 'Model Selection', icon: <Cpu size={20} /> },
    { id: 'results', label: 'Evaluation Results', icon: <LineChart size={20} /> },
    { id: 'experiments', label: 'MLOps & History', icon: <History size={20} /> },
  ];

  return (
    <div className="w-64 bg-slate-900 text-white flex flex-col h-full shadow-2xl">
      <div className="p-6 flex items-center gap-3 border-b border-slate-800">
        <div className="bg-primary-500 p-2 rounded-lg">
          <LayoutDashboard size={24} className="text-white" />
        </div>
        <div>
          <h1 className="font-bold text-xl tracking-tight leading-tight">MLA</h1>
          <p className="text-xs text-slate-400">Machine Learning Studio</p>
        </div>
      </div>
      
      <nav className="flex-1 py-6 px-4 space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
              activeTab === item.id 
                ? 'bg-primary-600/10 text-primary-400 shadow-sm border border-primary-500/20' 
                : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
            }`}
          >
            {item.icon}
            <span className="font-medium text-sm">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="p-6 border-t border-slate-800">
        <div className="bg-slate-800 rounded-lg p-4">
          <p className="text-xs text-slate-400 uppercase tracking-widest font-semibold mb-2">Status</p>
          <div className="flex items-center gap-2 text-sm text-green-400">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            System Online
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
