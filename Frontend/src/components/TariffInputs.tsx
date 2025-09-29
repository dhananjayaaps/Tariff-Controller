
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
    <form onSubmit={handleSubmit}>
      <label>
        Rate ($/kWh):
        <input
          type="number"
          value={config.rate}
          onChange={(e) => setConfig({ ...config, rate: parseFloat(e.target.value) })}
        />
      </label>
      <label>
        Fixed Fee ($):
        <input
          type="number"
          value={config.fixed_fee}
          onChange={(e) => setConfig({ ...config, fixed_fee: parseFloat(e.target.value) })}
        />
      </label>
      <button type="submit">Update Flat Tariff</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default TariffInputs;