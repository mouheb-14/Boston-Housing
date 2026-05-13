import React, { useState } from 'react';
import { Settings2, Info, Play, RefreshCw, UploadCloud, ChevronDown } from 'lucide-react';

const ALGORITHMS = {
  lr: { name: 'Linear Regression', desc: 'Simple linear approach for modeling the relationship between a dependent variable and one or more independent variables.' },
  svr: { name: 'Support Vector Regression (SVR)', desc: 'Versatile model that can handle non-linear relationships using kernels. Good for small to medium datasets.' },
  rf: { name: 'Random Forest Regression', desc: 'Powerful ensemble method that combines multiple decision trees to produce more robust predictions.' },
  knn: { name: 'KNN Regression', desc: 'Predicts the target value based on the average of its k-nearest neighbors in the feature space.' },
};

const ModelsView = () => {
  const [selectedAlgo, setSelectedAlgo] = useState('rf');
  const [trainingMode, setTrainingMode] = useState('scratch');

  const startTraining = async () => {
    try {
      const response = await fetch('http://localhost:8000/train', { method: 'POST' });
      const data = await response.json();
      alert("Entraînement lancé ! Les résultats apparaîtront dans l'onglet Experiments une fois terminés.");
    } catch (error) {
      console.error("Erreur lors du lancement de l'entraînement:", error);
      alert("Erreur de connexion au backend. Assurez-vous que l'API est lancée.");
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-end pb-4 border-b border-slate-200">
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">Model Selection & Configuration</h2>
          <p className="text-slate-500 mt-1">Configure your regression algorithms and tune hyperparameters.</p>
        </div>
        <div className="flex bg-slate-100 p-1 rounded-lg">
          <button 
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${trainingMode === 'scratch' ? 'bg-white shadow-sm text-primary-600' : 'text-slate-500'}`}
            onClick={() => setTrainingMode('scratch')}
          >
            Train from Scratch
          </button>
          <button 
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${trainingMode === 'pretrained' ? 'bg-white shadow-sm text-primary-600' : 'text-slate-500'}`}
            onClick={() => setTrainingMode('pretrained')}
          >
            Load Pre-trained
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column - Selection */}
        <div className="card-premium p-6 lg:col-span-1 border-t-4 border-t-primary-500">
          <h3 className="font-semibold text-lg flex items-center gap-2 mb-4">
            <Settings2 size={18} className="text-primary-500" /> Algorithm
          </h3>
          
          <div className="space-y-3">
            {Object.entries(ALGORITHMS).map(([key, info]) => (
              <div 
                key={key}
                onClick={() => setSelectedAlgo(key)}
                className={`relative p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                  selectedAlgo === key 
                    ? 'border-primary-500 bg-primary-50' 
                    : 'border-slate-100 hover:border-slate-300'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className={`font-medium ${selectedAlgo === key ? 'text-primary-700' : 'text-slate-700'}`}>
                    {info.name}
                  </span>
                  <div className="group relative">
                    <Info size={16} className="text-slate-400 cursor-help" />
                    {/* Tooltip */}
                    <div className="absolute right-0 bottom-full mb-2 w-48 p-2 bg-slate-800 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                      {info.desc}
                      <div className="absolute top-full right-2 border-4 border-transparent border-t-slate-800"></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column - Hyperparameters */}
        <div className="card-premium p-6 lg:col-span-2">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <RefreshCw size={18} className="text-primary-500" /> Hyperparameters
            </h3>
            <button className="btn-secondary text-sm flex items-center gap-2">
              Auto Tune <ChevronDown size={14} />
            </button>
          </div>

          <div className="bg-slate-50 rounded-xl border border-slate-100 p-6 min-h-[250px]">
            {selectedAlgo === 'knn' && (
              <div className="space-y-4 animate-in fade-in">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">n_neighbors (k)</label>
                  <input type="number" className="input-field max-w-xs" defaultValue={5} min={1} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">weights</label>
                  <select className="input-field max-w-xs cursor-pointer">
                    <option>uniform</option>
                    <option>distance</option>
                  </select>
                </div>
              </div>
            )}

            {selectedAlgo === 'rf' && (
              <div className="space-y-4 animate-in fade-in grid grid-cols-2 gap-4">
                <div className="col-span-2 md:col-span-1 mt-0">
                  <label className="block text-sm font-medium text-slate-700 mb-1">n_estimators</label>
                  <input type="number" className="input-field" defaultValue={100} />
                </div>
                <div className="col-span-2 md:col-span-1 mt-0">
                  <label className="block text-sm font-medium text-slate-700 mb-1">max_depth</label>
                  <input type="number" className="input-field" placeholder="None" />
                </div>
              </div>
            )}

            {selectedAlgo === 'svr' && (
              <div className="space-y-4 animate-in fade-in grid grid-cols-2 gap-4">
                <div className="col-span-2 md:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">C (Regularization)</label>
                  <input type="number" className="input-field" defaultValue={1.0} step={0.1} />
                </div>
                <div className="col-span-2 md:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">kernel</label>
                  <select className="input-field cursor-pointer">
                    <option>rbf</option>
                    <option>linear</option>
                    <option>poly</option>
                  </select>
                </div>
              </div>
            )}
            
            {selectedAlgo === 'lr' && (
              <div className="flex flex-col items-center justify-center h-full text-slate-400 py-10">
                <Settings2 size={48} className="mb-2 opacity-20" />
                <p>Simple Linear Regression. No custom hyperparameters available.</p>
              </div>
            )}
          </div>

          <div className="mt-8 flex justify-end">
            <button className="btn-primary flex items-center gap-2 px-8" onClick={startTraining}>
              <Play size={18} /> Start Training
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ModelsView;
