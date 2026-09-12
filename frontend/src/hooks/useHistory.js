import { useEffect, useState } from 'react';
import { getHistory } from '../services/historyService';

export function useHistory() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadHistory() {
      try {
        const data = await getHistory();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({ data: null, isLoading: false, error: error.response?.data?.detail || 'Unable to load history.' });
        }
      }
    }

    loadHistory();
    return () => { isMounted = false; };
  }, []);

  return state;
}
