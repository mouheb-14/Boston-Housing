import React from 'react';
import { Tag, Rewind, CheckCircle, Clock } from 'lucide-react';

const ExperimentsView = () => {
  const versions = [
    { id: 'v1.4.2', model: 'Random Forest', status: 'Production', date: '2 hours ago', metrics: 'Acc: 94% | F1: 0.92', current: true },
    { id: 'v1.4.1', model: 'SVM', status: 'Archived', date: '1 day ago', metrics: 'Acc: 89% | F1: 0.88', current: false },
    { id: 'v1.4.0', model: 'KNN', status: 'Archived', date: '3 days ago', metrics: 'Acc: 82% | F1: 0.80', current: false },
    { id: 'v1.3.5', model: 'Logistic Regression', status: 'Archived', date: '1 week ago', metrics: 'Acc: 78% | F1: 0.76', current: false },
  ];

  return (
    <div className="space-y-6 fade-in">
      <div className="pb-4 border-b border-slate-200">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">MLOps & History</h2>
        <p className="text-slate-500 mt-1">Track model experiments, compare versions, and manage deployments.</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div className="card-premium overflow-hidden">
          <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
             <h3 className="font-semibold text-slate-800 flex items-center gap-2">
              <Clock size={18} className="text-primary-500" /> Experiment Log
            </h3>
          </div>
          
          <div className="divide-y divide-slate-100">
            {versions.map((ver, idx) => (
              <div key={idx} className={`p-6 flex items-center justify-between hover:bg-slate-50 transition duration-150 ${ver.current ? 'bg-primary-50/30' : ''}`}>
                <div className="flex items-start gap-4 text-sm w-1/3">
                  <div className={`p-2 rounded-lg ${ver.current ? 'bg-primary-100 text-primary-600' : 'bg-slate-100 text-slate-500'}`}>
                    <Tag size={20} />
                  </div>
                  <div>
                    <span className="font-bold text-slate-800 block text-base">{ver.id}</span>
                    <span className="text-slate-500 flex items-center gap-1 mt-1">
                      {ver.current && <CheckCircle size={12} className="text-primary-500" />} 
                      {ver.model}
                    </span>
                  </div>
                </div>

                <div className="text-sm text-slate-600 font-medium w-1/3 text-center bg-white border border-slate-200 py-1.5 px-3 rounded-md shadow-sm">
                  {ver.metrics}
                </div>

                <div className="flex items-center justify-end gap-3 w-1/3">
                  <span className="text-xs text-slate-400 font-medium">{ver.date}</span>
                  {!ver.current ? (
                    <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded bg-orange-50 text-orange-600 hover:bg-orange-100 transition border border-orange-200 shadow-sm ml-4">
                      <Rewind size={14} /> Rollback
                    </button>
                  ) : (
                    <span className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded bg-green-50 text-green-700 border border-green-200 ml-4 shadow-sm">
                      <span className="relative flex h-2 w-2 mr-1">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                      </span>
                      Active
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
    </div>
  );
};

export default ExperimentsView;
