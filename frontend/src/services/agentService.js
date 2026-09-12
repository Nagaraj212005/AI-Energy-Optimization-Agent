import apiClient from './api';

export async function askAgent(question) {
  const response = await apiClient.post('/agent/', { question });
  return response.data;
}
