import { useEffect, useState } from 'react';
import { getReport } from '../services/reportService';

export function useReport() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadReport() {
      try {
        const data = await getReport();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({ data: null, isLoading: false, error: error.response?.data?.detail || 'Unable to load report.' });
        }
      }
    }

    loadReport();
    return () => { isMounted = false; };
  }, []);

  return state;
}
