"use client";
import { useState } from 'react';
import { calculateBill } from '../utils/api';

const ModelSelector = ({ onCalculateSuccess }: { onCalculateSuccess: () => void }) => {
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [bill, setBill] = useState<number | null>(null);

  const handleCalculate = async () => {
    if (selectedModel) {
      const response = await calculateBill(selectedModel);
      setBill(response.data.bill);
      onCalculateSuccess(); // Trigger refetch after successful calculation
    }
  };

  return (
    <div id="calculate" className="mb-6">
      <h2 className="text-xl font-bold mb-2">Select Model</h2>
      <div className="space-y-4">
        <select
          onChange={(e) => setSelectedModel(e.target.value)}
          value={selectedModel || ''}
          className="w-full p-2 border rounded"
        >
          <option value="">Select Model</option>
          <option value="flat">Flat Rate</option>
          <option value="tou">Time-of-Use</option>
          <option value="tiered">Tiered</option>
        </select>
        <button
          onClick={handleCalculate}
          className="bg-green-500 text-white p-2 rounded hover:bg-green-600 w-full"
        >
          Calculate Bill
        </button>
        {bill && <p className="mt-2 text-lg">Bill: ${bill.toFixed(2)}</p>}
      </div>
    </div>
  );
};

export default ModelSelector;