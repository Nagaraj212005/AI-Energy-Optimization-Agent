import { useEffect, useState } from 'react';
import { getForecast } from '../services/forecastService';

export function useForecast() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadForecast() {
      try {
        const data = await getForecast();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({
            data: null,
            isLoading: false,
            error: error.response?.data?.detail || 'Unable to load forecast data.',
          });
        }
      }
    }

    loadForecast();
    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
