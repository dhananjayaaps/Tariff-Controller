
"use client";
import { useState } from 'react';
import { updateTariff } from '../utils/api';

const TariffInputs = () => {
  const [config, setConfig] = useState({ rate: 0.25, fixed_fee: 10 });
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await updateTariff('flat', config);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Update failed');
    }
  };

  return (
    <div id="calculate" className="mb-6">
      <h2 className="text-xl font-bold mb-2">Tariff Inputs</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700">Rate ($/kWh)</label>
          <input
            type="number"
            step="0.01"
            value={config.rate}
            onChange={(e) => setConfig({ ...config, rate: parseFloat(e.target.value) })}
            className="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label className="block text-gray-700">Fixed Fee ($)</label>
          <input
            type="number"
            step="0.01"
            value={config.fixed_fee}
            onChange={(e) => setConfig({ ...config, fixed_fee: parseFloat(e.target.value) })}
            className="w-full p-2 border rounded"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Update Tariff</button>
      </form>
      {message && <p className="mt-2 text-green-600">{message}</p>}
    </div>
  );
};

export default TariffInputs;