"use client";
import { useEffect, useState } from 'react';
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from 'chart.js';
import { getUsageTrend } from '../utils/api';
import { UsageTrend } from '../types';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend);

const Visualization = () => {
  const [trendData, setTrendData] = useState<UsageTrend[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getUsageTrend();
      setTrendData(response.data.trend);
    };
    fetchData();
  }, []);

  const data = {
    labels: trendData.map(d => d.timestamp),
    datasets: [{
      label: 'kWh Usage',
      data: trendData.map(d => d.kWh),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };

  const options = {
    responsive: true,
    plugins: { legend: { position: "top" as const }, title: { display: true, text: 'Usage Trend' } }
  };

  return (
    <div>
      <Chart type="line" data={data} options={options} />
      <div style={{ height: '200px', border: '1px solid #ccc', marginTop: '20px' }}>Bill Breakdown (Placeholder)</div>
    </div>
  );
};

export default Visualization;