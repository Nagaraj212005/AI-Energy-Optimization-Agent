import apiClient from './api';

export async function getRecommendations() {
  const response = await apiClient.get('/recommendation/');
  return response.data;
}
