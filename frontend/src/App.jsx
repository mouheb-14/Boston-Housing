import React, { useState } from 'react';
import { Database, LineChart, Cpu, History, Settings, Box } from 'lucide-react';
import Sidebar from './components/Sidebar';
import ModelsView from './components/views/ModelsView';
import DataView from './components/views/DataView';
import ResultsView from './components/views/ResultsView';
import ExperimentsView from './components/views/ExperimentsView';

function App() {
  const [activeTab, setActiveTab] = useState('models');

  const renderContent = () => {
    switch (activeTab) {
      case 'data':
        return <DataView />;
      case 'models':
        return <ModelsView />;
      case 'results':
        return <ResultsView />;
      case 'experiments':
        return <ExperimentsView />;
      default:
        return <ModelsView />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-800">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="max-w-6xl mx-auto">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

export default App;
