"use client";
import { useState } from 'react';
import { calculateBill } from '../utils/api';

const ModelSelector = () => {
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [bill, setBill] = useState<number | null>(null);

  const handleCalculate = async () => {
    if (selectedModel) {
      const response = await calculateBill(selectedModel);
      setBill(response.data.bill);
    }
  };

  return (
    <div>
      <select onChange={(e) => setSelectedModel(e.target.value)} value={selectedModel || ''}>
        <option value="">Select Model</option>
        <option value="flat">Flat Rate</option>
        <option value="tou">Time-of-Use</option>
        <option value="tiered">Tiered</option>
      </select>
      <button onClick={handleCalculate}>Calculate</button>
      {bill && <p>Bill: ${bill.toFixed(2)}</p>}
    </div>
  );
};

export default ModelSelector;