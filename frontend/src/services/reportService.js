import apiClient from './api';

export async function getReport() {
  const response = await apiClient.get('/report/');
  return response.data;
}
