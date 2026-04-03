import React from 'react';
import { UploadCloud, Trash2, Filter, Download } from 'lucide-react';

const DataView = () => {
  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-end pb-4 border-b border-slate-200">
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">Dataset Management</h2>
          <p className="text-slate-500 mt-1">Upload, preview and clean your training data before feeding the models.</p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <UploadCloud size={18} /> Upload Dataset
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="card-premium p-4 md:col-span-1 flex flex-col gap-3">
          <h3 className="font-semibold text-slate-700 text-sm uppercase tracking-wider mb-2">Quick Cleaning</h3>
          <button className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 hover:bg-slate-100 p-2 rounded border border-slate-200 transition">
            <Trash2 size={16} className="text-red-400" /> Remove Nulls
          </button>
          <button className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 hover:bg-slate-100 p-2 rounded border border-slate-200 transition">
            <Filter size={16} className="text-blue-400" /> Drop Duplicates
          </button>
          <button className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 hover:bg-slate-100 p-2 rounded border border-slate-200 transition">
            <Download size={16} className="text-green-400" /> Export Clean Data
          </button>
        </div>

        <div className="card-premium p-0 md:col-span-3 overflow-hidden">
          <div className="bg-slate-50 px-6 py-3 border-b border-slate-100 flex justify-between items-center">
            <h3 className="font-semibold text-slate-700">Data Preview <span className="text-xs text-slate-400 font-normal ml-2">10,423 rows • 14 columns</span></h3>
            <div className="text-xs text-slate-400 bg-white px-2 py-1 rounded border border-slate-200 cursor-pointer">
              Select Columns
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 whitespace-nowrap"><input type="checkbox" className="rounded text-primary-500" /></th>
                  <th className="px-6 py-3">ID</th>
                  <th className="px-6 py-3">crim</th>
                  <th className="px-6 py-3">zn</th>
                  <th className="px-6 py-3">indus</th>
                  <th className="px-6 py-3">chas</th>
                  <th className="px-6 py-3">nox</th>
                  <th className="px-6 py-3">rm</th>
                  <th className="px-6 py-3">medv (Target)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-3"><input type="checkbox" className="rounded text-primary-500" /></td>
                  <td className="px-6 py-3 text-slate-500">1</td>
                  <td className="px-6 py-3">0.00632</td>
                  <td className="px-6 py-3">18.0</td>
                  <td className="px-6 py-3">2.31</td>
                  <td className="px-6 py-3">0</td>
                  <td className="px-6 py-3">0.538</td>
                  <td className="px-6 py-3 font-medium">6.575</td>
                  <td className="px-6 py-3">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">24.0</span>
                  </td>
                </tr>
                <tr className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-3"><input type="checkbox" className="rounded text-primary-500" /></td>
                  <td className="px-6 py-3 text-slate-500">2</td>
                  <td className="px-6 py-3">0.02731</td>
                  <td className="px-6 py-3">0.0</td>
                  <td className="px-6 py-3">7.07</td>
                  <td className="px-6 py-3">0</td>
                  <td className="px-6 py-3">0.469</td>
                  <td className="px-6 py-3 font-medium">6.421</td>
                  <td className="px-6 py-3">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">21.6</span>
                  </td>
                </tr>
                <tr className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-3"><input type="checkbox" className="rounded text-primary-500" /></td>
                  <td className="px-6 py-3 text-slate-500">4</td>
                  <td className="px-6 py-3">0.03237</td>
                  <td className="px-6 py-3">0.0</td>
                  <td className="px-6 py-3">2.18</td>
                  <td className="px-6 py-3">0</td>
                  <td className="px-6 py-3">0.458</td>
                  <td className="px-6 py-3 font-medium">6.998</td>
                  <td className="px-6 py-3">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">33.4</span>
                  </td>
                </tr>
                <tr className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-3"><input type="checkbox" className="rounded text-primary-500" /></td>
                  <td className="px-6 py-3 text-slate-500">5</td>
                  <td className="px-6 py-3">0.06905</td>
                  <td className="px-6 py-3">0.0</td>
                  <td className="px-6 py-3">2.18</td>
                  <td className="px-6 py-3">0</td>
                  <td className="px-6 py-3">0.458</td>
                  <td className="px-6 py-3 font-medium">7.147</td>
                  <td className="px-6 py-3">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">36.2</span>
                  </td>
                </tr>
                <tr className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-3"><input type="checkbox" className="rounded text-primary-500" /></td>
                  <td className="px-6 py-3 text-slate-500">7</td>
                  <td className="px-6 py-3">0.08829</td>
                  <td className="px-6 py-3">12.5</td>
                  <td className="px-6 py-3">7.87</td>
                  <td className="px-6 py-3">0</td>
                  <td className="px-6 py-3">0.524</td>
                  <td className="px-6 py-3 font-medium">6.012</td>
                  <td className="px-6 py-3">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">22.9</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataView;
