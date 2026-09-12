import { useEffect, useState } from 'react';
import { getRecommendations } from '../services/recommendationService';

export function useRecommendations() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadRecommendations() {
      try {
        const data = await getRecommendations();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({
            data: null,
            isLoading: false,
            error: error.response?.data?.detail || 'Unable to load recommendations.',
          });
        }
      }
    }

    loadRecommendations();
    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
