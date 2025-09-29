"use client";
import { useState } from 'react';
import { updateTariff } from '../utils/api';

interface FlatConfig {
  rate: number;
  fixed_fee: number;
}

interface TouConfig {
  peakHours: number[][];
  peakRate: number;
  shoulderRate: number;
  offpeakRate: number;
  fixedFee: number;
}

interface TieredConfig {
  tiers: number[][];
  fixedFee: number;
}

// Combined config type with index signature
interface TariffConfig {
  flat: FlatConfig;
  tou: TouConfig;
  tiered: TieredConfig;
}

const TariffConfig = ({ onConfigUpdate }: { onConfigUpdate: () => void }) => {
  const [activeTab, setActiveTab] = useState<'flat' | 'tou' | 'tiered'>('flat');
  const [config, setConfig] = useState<TariffConfig>({
    flat: { rate: 0.25, fixed_fee: 10 },
    tou: { peakHours: [[18, 22]], peakRate: 0.40, shoulderRate: 0.25, offpeakRate: 0.15, fixedFee: 10 },
    tiered: { tiers: [[100, 0.20], [300, 0.30], [Number.POSITIVE_INFINITY, 0.40]], fixedFee: 10 }
  });
  const [message, setMessage] = useState<string | null>(null);

  const handleAddPeakHour = () => {
    setConfig(prev => ({
      ...prev,
      tou: { ...prev.tou, peakHours: [...prev.tou.peakHours, [0, 0]] }
    }));
  };

  const handleAddTier = () => {
    setConfig(prev => ({
      ...prev,
      tiered: { ...prev.tiered, tiers: [...prev.tiered.tiers, [0, 0.0]] }
    }));
  };

  const handleUpdateField = (tariff: 'flat' | 'tou' | 'tiered', field: string, value: any, index?: number) => {
    setConfig(prev => {
      if (tariff === 'tou' && field.startsWith('peakHours')) {
        const [i, subField] = field.split('_');
        const newPeakHours = [...prev.tou.peakHours];
        newPeakHours[parseInt(i)] = [...newPeakHours[parseInt(i)]];
        newPeakHours[parseInt(i)][subField === 'start' ? 0 : 1] = value;
        return { ...prev, tou: { ...prev.tou, peakHours: newPeakHours } };
      } else if (tariff === 'tiered' && field.startsWith('tiers')) {
        const [i, subField] = field.split('_');
        const newTiers = [...prev.tiered.tiers];
        newTiers[parseInt(i)] = [...newTiers[parseInt(i)]];
        newTiers[parseInt(i)][subField === 'threshold' ? 0 : 1] = value;
        return { ...prev, tiered: { ...prev.tiered, tiers: newTiers } };
      }
      return { ...prev, [tariff]: { ...prev[tariff], [field]: value } };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      let response;
      if (activeTab === 'flat') {
        response = await updateTariff('flat', { rate: config.flat.rate, fixed_fee: config.flat.fixed_fee });
      } else if (activeTab === 'tou') {
        response = await updateTariff('tou', {
          peak_hours: config.tou.peakHours,
          peak_rate: config.tou.peakRate,
          shoulder_rate: config.tou.shoulderRate,
          offpeak_rate: config.tou.offpeakRate,
          fixed_fee: config.tou.fixedFee
        });
      } else if (activeTab === 'tiered') {
        response = await updateTariff('tiered', { tiers: config.tiered.tiers, fixed_fee: config.tiered.fixedFee });
      }
      setMessage(response?.data?.message || 'Update successful');
      onConfigUpdate();
    } catch (error) {
      setMessage('Update failed: ' + (error as Error).message);
    }
  };

  return (
    <div id="calculate" className="mb-6">
      <h2 className="text-xl font-bold mb-2">Configure Tariffs</h2>
      <div className="mb-4">
        <button
          onClick={() => setActiveTab('flat')}
          className={`mr-2 px-4 py-2 rounded ${activeTab === 'flat' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Flat
        </button>
        <button
          onClick={() => setActiveTab('tou')}
          className={`mr-2 px-4 py-2 rounded ${activeTab === 'tou' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          TOU
        </button>
        <button
          onClick={() => setActiveTab('tiered')}
          className={`px-4 py-2 rounded ${activeTab === 'tiered' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Tiered
        </button>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        {activeTab === 'flat' && (
          <>
            <div>
              <label className="block text-gray-700">Rate ($/kWh)</label>
              <input
                type="number"
                step="0.01"
                value={config.flat.rate}
                onChange={(e) => handleUpdateField('flat', 'rate', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-gray-700">Fixed Fee ($)</label>
              <input
                type="number"
                step="0.01"
                value={config.flat.fixed_fee}
                onChange={(e) => handleUpdateField('flat', 'fixed_fee', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
          </>
        )}
        {activeTab === 'tou' && (
          <>
            {config.tou.peakHours.map((hour, index) => (
              <div key={index} className="flex space-x-2">
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={hour[0]}
                  onChange={(e) => handleUpdateField('tou', `peakHours_${index}_start`, parseInt(e.target.value))}
                  className="w-20 p-2 border rounded"
                  placeholder="Start Hour"
                />
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={hour[1]}
                  onChange={(e) => handleUpdateField('tou', `peakHours_${index}_end`, parseInt(e.target.value))}
                  className="w-20 p-2 border rounded"
                  placeholder="End Hour"
                />
              </div>
            ))}
            <button
              type="button"
              onClick={handleAddPeakHour}
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Add Peak Period
            </button>
            <div>
              <label className="block text-gray-700">Peak Rate ($/kWh)</label>
              <input
                type="number"
                step="0.01"
                value={config.tou.peakRate}
                onChange={(e) => handleUpdateField('tou', 'peakRate', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-gray-700">Shoulder Rate ($/kWh)</label>
              <input
                type="number"
                step="0.01"
                value={config.tou.shoulderRate}
                onChange={(e) => handleUpdateField('tou', 'shoulderRate', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-gray-700">Off-Peak Rate ($/kWh)</label>
              <input
                type="number"
                step="0.01"
                value={config.tou.offpeakRate}
                onChange={(e) => handleUpdateField('tou', 'offpeakRate', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-gray-700">Fixed Fee ($)</label>
              <input
                type="number"
                step="0.01"
                value={config.tou.fixedFee}
                onChange={(e) => handleUpdateField('tou', 'fixedFee', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
          </>
        )}
        {activeTab === 'tiered' && (
          <>
            {config.tiered.tiers.map((tier, index) => (
              <div key={index} className="flex space-x-2">
                <input
                  type="number"
                  value={tier[0] === Number.POSITIVE_INFINITY ? '' : tier[0]}
                  onChange={(e) => handleUpdateField('tiered', `tiers_${index}_threshold`, e.target.value === '' ? Number.POSITIVE_INFINITY : parseFloat(e.target.value))}
                  className="w-40 p-2 border rounded"
                  placeholder="Threshold (kWh)"
                />
                <input
                  type="number"
                  step="0.01"
                  value={tier[1]}
                  onChange={(e) => handleUpdateField('tiered', `tiers_${index}_rate`, parseFloat(e.target.value))}
                  className="w-40 p-2 border rounded"
                  placeholder="Rate ($/kWh)"
                />
              </div>
            ))}
            <button
              type="button"
              onClick={handleAddTier}
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Add Tier
            </button>
            <div>
              <label className="block text-gray-700">Fixed Fee ($)</label>
              <input
                type="number"
                step="0.01"
                value={config.tiered.fixedFee}
                onChange={(e) => handleUpdateField('tiered', 'fixedFee', parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
          </>
        )}
        <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Update Tariff</button>
      </form>
      {message && <p className="mt-2 text-green-600">{message}</p>}
    </div>
  );
};

export default TariffConfig;