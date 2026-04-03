import React from 'react';
import { DownloadCloud, ExternalLink } from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ResultsView = () => {

  const performanceOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: false },
    },
  };

  const performanceData = {
    labels: ['Random Forest', 'SVM', 'KNN', 'Logistic Reg.'],
    datasets: [
      {
        label: 'Accuracy',
        data: [0.94, 0.89, 0.82, 0.78],
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
      },
      {
        label: 'F1-Score',
        data: [0.92, 0.88, 0.80, 0.76],
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
      },
    ],
  };

  const rocData = {
    labels: ['0', '0.2', '0.4', '0.6', '0.8', '1.0'],
    datasets: [
      {
        label: 'Random Forest (AUC = 0.96)',
        data: [0, 0.85, 0.92, 0.96, 0.98, 1.0],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.5)',
        tension: 0.4,
      },
      {
        label: 'Baseline',
        data: [0, 0.2, 0.4, 0.6, 0.8, 1.0],
        borderColor: 'rgb(203, 213, 225)',
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      }
    ],
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-end pb-4 border-b border-slate-200">
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">Evaluation Results</h2>
          <p className="text-slate-500 mt-1">Review model performance, confusion matrices, and ROC curves.</p>
        </div>
        <button className="btn-secondary flex items-center gap-2">
          <DownloadCloud size={18} /> Export PDF Report
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Performance Comparison */}
        <div className="card-premium p-6">
          <h3 className="font-semibold text-lg text-slate-800 mb-4">Performance Comparison</h3>
          <div className="h-64 w-full flex items-center justify-center">
            <Bar options={performanceOptions} data={performanceData} />
          </div>
        </div>

        {/* ROC Curve */}
        <div className="card-premium p-6">
          <h3 className="font-semibold text-lg text-slate-800 mb-4">ROC Curve</h3>
          <div className="h-64 w-full flex items-center justify-center">
            <Line options={{responsive: true, maintainAspectRatio: false}} data={rocData} height={256} />
          </div>
        </div>

        {/* Confusion Matrix (Placeholder) */}
        <div className="card-premium p-6 lg:col-span-2">
           <h3 className="font-semibold text-lg text-slate-800 mb-4 flex justify-between">
            Confusion Matrix (Random Forest)
            <button className="text-primary-600 text-sm font-medium hover:underline flex items-center gap-1">
              View Detailed Metrics <ExternalLink size={14} />
            </button>
          </h3>
          <div className="flex items-center justify-center bg-slate-50 border border-slate-100 rounded-xl py-8">
            {/* CSS Grid based fake heat map */}
            <div className="inline-grid grid-cols-3 gap-1 grid-rows-3 text-sm text-center">
              <div></div>
              <div className="font-medium text-slate-500 p-2">Predicted Postive</div>
              <div className="font-medium text-slate-500 p-2">Predicted Negative</div>
              
              <div className="font-medium text-slate-500 flex items-center justify-end px-4">Actual Positive</div>
              <div className="bg-primary-500 text-white p-6 rounded shadow flex flex-col justify-center">
                <span className="text-xl font-bold">142</span>
                <span className="text-xs opacity-80 mt-1">True Positives</span>
              </div>
              <div className="bg-red-100 text-red-800 p-6 rounded shadow flex flex-col justify-center">
                <span className="text-xl font-bold">12</span>
                <span className="text-xs opacity-80 mt-1">False Negatives</span>
              </div>

              <div className="font-medium text-slate-500 flex items-center justify-end px-4">Actual Negative</div>
              <div className="bg-orange-100 text-orange-800 p-6 rounded shadow flex flex-col justify-center">
                <span className="text-xl font-bold">8</span>
                <span className="text-xs opacity-80 mt-1">False Positives</span>
              </div>
              <div className="bg-primary-600 text-white p-6 rounded shadow flex flex-col justify-center">
                <span className="text-xl font-bold">1,024</span>
                <span className="text-xs opacity-80 mt-1">True Negatives</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ResultsView;
