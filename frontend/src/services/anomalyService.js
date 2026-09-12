import apiClient from './api';

export async function getAnomalies() {
  const response = await apiClient.get('/anomaly/');
  return response.data;
}
