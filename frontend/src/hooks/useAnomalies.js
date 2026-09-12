import { useEffect, useState } from 'react';
import { getAnomalies } from '../services/anomalyService';

export function useAnomalies() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadAnomalies() {
      try {
        const data = await getAnomalies();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({
            data: null,
            isLoading: false,
            error: error.response?.data?.detail || 'Unable to load anomaly data.',
          });
        }
      }
    }

    loadAnomalies();
    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
