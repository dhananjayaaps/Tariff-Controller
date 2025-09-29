import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
});

export const uploadFile = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload', formData);
};

export const calculateBill = (tariffType: string) =>
  api.post('/calculate_bill', { tariff_type: tariffType });

export const compareTariffs = () => api.get('/compare_tariffs');

export const getUsageTrend = () => api.get('/get_usage_trend');

export const updateTariff = (tariffType: string, config: any) =>
  api.post('/update_tariff', { tariff_type: tariffType, config });