import apiClient from './api';

export async function getForecast() {
  const response = await apiClient.get('/forecast/');
  return response.data;
}
