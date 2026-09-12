import {
  BarChart3,
  Bot,
  FileBarChart,
  Gauge,
  History,
  Lightbulb,
  ShieldAlert,
} from 'lucide-react';

export const navigationItems = [
  { label: 'Dashboard', path: '/', icon: Gauge },
  { label: 'Forecast', path: '/forecast', icon: BarChart3 },
  { label: 'Anomaly Detection', path: '/anomaly', icon: ShieldAlert },
  { label: 'Recommendations', path: '/recommendations', icon: Lightbulb },
  { label: 'History', path: '/history', icon: History },
  { label: 'Reports', path: '/reports', icon: FileBarChart },
  { label: 'AI Assistant', path: '/assistant', icon: Bot },
];
