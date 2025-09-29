"use client";
import { useEffect, useState } from 'react';
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend, BarElement } from 'chart.js';
import { getUsageTrend, compareTariffs } from '../utils/api';
import { UsageTrend, BillResponse } from '../types';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend, BarElement);

const Visualization = () => {
  const [trendData, setTrendData] = useState<UsageTrend[]>([]);
  const [comparison, setComparison] = useState<Record<string, BillResponse> | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const trendResponse = await getUsageTrend();
      setTrendData(trendResponse.data.trend);
      const compareResponse = await compareTariffs();
      setComparison(compareResponse.data.comparison);
    };
    fetchData();
  }, []);

  const lineData = {
    labels: trendData.map(d => d.timestamp),
    datasets: [{
      label: 'kWh Usage',
      data: trendData.map(d => d.kWh),
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.1
    }]
  };

  const barData = comparison ? {
    labels: Object.keys(comparison),
    datasets: [{
      label: 'Bill Amount ($)',
      data: Object.values(comparison).map(c => c.bill),
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  } : { labels: [], datasets: [] };

  const options = { responsive: true, plugins: { legend: { position: "top" as const }, title: { display: true } } };

  return (
    <div id="reports" className="mb-6">
      <h2 className="text-xl font-bold mb-2">Visualizations</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg font-semibold">Usage Trend</h3>
          <Chart type="line" data={lineData} options={options} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg font-semibold">Bill Comparison</h3>
          <Chart type="bar" data={barData} options={options} />
        </div>
      </div>
    </div>
  );
};

export default Visualization;