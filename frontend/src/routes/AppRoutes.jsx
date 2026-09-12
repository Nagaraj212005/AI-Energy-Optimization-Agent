import { Route, Routes } from 'react-router-dom';
import AppLayout from '../layouts/AppLayout';
import AnomalyPage from '../pages/AnomalyPage';
import AssistantPage from '../pages/AssistantPage';
import DashboardPage from '../pages/DashboardPage';
import ForecastPage from '../pages/ForecastPage';
import HistoryPage from '../pages/HistoryPage';
import PagePlaceholder from '../pages/PagePlaceholder';
import ReportPage from '../pages/ReportPage';
import RecommendationsPage from '../pages/RecommendationsPage';

const pages = {
  dashboard: {
    eyebrow: 'Workspace overview',
    title: 'Energy intelligence, at a glance.',
    description: 'Your live consumption metrics, forecasts, and optimization opportunities will appear here.',
  },
  forecast: {
    eyebrow: 'Forecast',
    title: 'Plan ahead with confidence.',
    description: 'Forecasting insights will be connected to the FastAPI service here.',
  },
  anomaly: {
    eyebrow: 'Anomaly detection',
    title: 'Spot what needs attention.',
    description: 'Unusual consumption patterns and severity signals will be surfaced here.',
  },
  recommendations: {
    eyebrow: 'Recommendations',
    title: 'Turn insight into action.',
    description: 'AI-generated energy optimization recommendations will appear here.',
  },
  history: {
    eyebrow: 'History',
    title: 'Explore your energy story.',
    description: 'Historical consumption records and filters will be connected here.',
  },
  reports: {
    eyebrow: 'Reports',
    title: 'A clearer view of performance.',
    description: 'Summary reports and export actions will be available here.',
  },
  assistant: {
    eyebrow: 'AI assistant',
    title: 'Ask better questions about energy.',
    description: 'Your optimization copilot will be connected to the agent endpoint here.',
  },
};

function Placeholder({ page }) {
  const content = pages[page];
  return <PagePlaceholder {...content} />;
}

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="forecast" element={<ForecastPage />} />
        <Route path="anomaly" element={<AnomalyPage />} />
        <Route path="recommendations" element={<RecommendationsPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="reports" element={<ReportPage />} />
        <Route path="assistant" element={<AssistantPage />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
