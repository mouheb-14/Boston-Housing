import React, { useState, useEffect } from 'react';
import { Tag, Rewind, CheckCircle, Clock, RefreshCw } from 'lucide-react';

const ExperimentsView = () => {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchExperiments = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/experiments');
      const data = await response.json();
      if (Array.isArray(data)) {
        setRuns(data);
      }
    } catch (error) {
      console.error("Erreur lors de la récupération des expériences:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExperiments();
  }, []);

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-center pb-4 border-b border-slate-200">
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">MLOps & History</h2>
          <p className="text-slate-500 mt-1">Track model experiments and compare regression metrics (from MLflow).</p>
        </div>
        <button 
          onClick={fetchExperiments}
          className="p-2 text-slate-500 hover:text-primary-600 transition-colors"
          title="Rafraîchir"
        >
          <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div className="card-premium overflow-hidden">
          <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
             <h3 className="font-semibold text-slate-800 flex items-center gap-2">
              <Clock size={18} className="text-primary-500" /> Experiment Log
            </h3>
          </div>
          
          <div className="divide-y divide-slate-100">
            {runs.length === 0 ? (
              <div className="p-10 text-center text-slate-400">
                <Tag size={48} className="mx-auto mb-2 opacity-10" />
                <p>Aucune expérience trouvée. Lancez un entraînement pour commencer !</p>
              </div>
            ) : (
              runs.map((run, idx) => (
                <div key={idx} className="p-6 flex items-center justify-between hover:bg-slate-50 transition duration-150">
                  <div className="flex items-start gap-4 text-sm w-1/4">
                    <div className="p-2 rounded-lg bg-slate-100 text-slate-500">
                      <Tag size={20} />
                    </div>
                    <div>
                      <span className="font-bold text-slate-800 block text-base truncate max-w-[150px]" title={run.id}>
                        {run.id.substring(0, 8)}...
                      </span>
                      <span className="text-slate-500 mt-1 block">
                        {run.name}
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-col gap-1 w-2/5">
                    <div className="flex gap-2">
                      <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs font-bold rounded">
                        R2: {run.metrics.R2?.toFixed(4) || 'N/A'}
                      </span>
                      <span className="px-2 py-1 bg-amber-50 text-amber-700 text-xs font-bold rounded">
                        MAE: {run.metrics.MAE?.toFixed(2) || 'N/A'}
                      </span>
                      <span className="px-2 py-1 bg-rose-50 text-rose-700 text-xs font-bold rounded">
                        MSE: {run.metrics.MSE?.toFixed(2) || 'N/A'}
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-400">Params: {JSON.stringify(run.params)}</p>
                  </div>

                  <div className="flex items-center justify-end gap-3 w-1/4">
                    <span className="text-xs text-slate-400 font-medium">
                      {new Date(run.start_time).toLocaleDateString()}
                    </span>
                    <span className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded bg-green-50 text-green-700 border border-green-200 shadow-sm">
                      Completed
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExperimentsView;
