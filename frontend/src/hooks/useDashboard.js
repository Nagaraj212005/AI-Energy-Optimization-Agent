import { useEffect, useState } from 'react';
import { getDashboardSummary } from '../services/dashboardService';

export function useDashboard() {
  const [state, setState] = useState({ data: null, isLoading: true, error: null });

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard() {
      try {
        const data = await getDashboardSummary();
        if (isMounted) {
          setState({ data, isLoading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({
            data: null,
            isLoading: false,
            error: error.response?.data?.detail || 'Unable to load dashboard data.',
          });
        }
      }
    }

    loadDashboard();
    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
