import { Activity, Database, Gauge, TrendingUp } from 'lucide-react';
import { useMemo } from 'react';
import ForecastChart from '../components/ForecastChart';
import PanelState from '../components/PanelState';
import StatCard from '../components/StatCard';
import { useDashboard } from '../hooks/useDashboard';
import { useForecast } from '../hooks/useForecast';
import { useHistory } from '../hooks/useHistory';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

function DashboardPage() {
  const { data, isLoading, error } = useDashboard();
  const forecastState = useForecast();
  const historyState = useHistory();
  const regionalTotals = useMemo(() => {
    const totals = (historyState.data?.history || []).reduce((result, row) => {
      result[row.region] = (result[row.region] || 0) + row.consumption;
      return result;
    }, {});
    return Object.entries(totals).sort(([, first], [, second]) => second - first).slice(0, 5);
  }, [historyState.data]);
  const regionBarWidths = ['w-full', 'w-4/5', 'w-3/5', 'w-2/5', 'w-1/4'];

  if (isLoading) {
    return (
      <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
        <div className="h-10 w-64 animate-pulse rounded-lg bg-white/[0.06]" />
        <div className="mt-3 h-4 w-96 max-w-full animate-pulse rounded bg-white/[0.04]" />
        <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[1, 2, 3, 4].map((item) => <div key={item} className="h-36 animate-pulse rounded-2xl bg-card" />)}
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
        <PanelState title="Dashboard unavailable" message={error} tone="error" />
      </section>
    );
  }

  if (!data || Object.keys(data).length === 0) {
    return (
      <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
        <PanelState title="No dashboard data" message="The API returned an empty summary. Check the data source and try again." />
      </section>
    );
  }

  const stats = [
    { label: 'Total consumption', value: numberFormatter.format(data.total_consumption), suffix: 'kWh', icon: Activity, accent: 'bg-blue-400/10 text-blue-300' },
    { label: 'Average consumption', value: numberFormatter.format(data.average_consumption), suffix: 'kWh', icon: Gauge, accent: 'bg-emerald-400/10 text-emerald-300' },
    { label: 'Peak consumption', value: numberFormatter.format(data.peak_consumption), suffix: 'kWh', icon: TrendingUp, accent: 'bg-amber-400/10 text-amber-300' },
    { label: 'Total records', value: numberFormatter.format(data.total_records), icon: Database, accent: 'bg-cyan-400/10 text-cyan-300' },
  ];

  return (
    <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">Workspace overview</p>
        <div className="mt-3 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">Energy intelligence, at a glance.</h1>
            <p className="mt-2 text-sm text-slate-500">A live summary of the energy data currently connected to your workspace.</p>
          </div>
            <div className="flex flex-wrap items-center gap-3 sm:justify-end"><span className="flex items-center gap-1.5 text-[11px] text-slate-500"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />Updated just now</span><span className="w-fit rounded-full border border-emerald-400/20 bg-emerald-400/[0.06] px-3 py-1.5 text-xs text-emerald-300">Live summary</span></div>
        </div>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => <StatCard key={stat.label} {...stat} />)}
      </div>

      <div className="mt-8 grid gap-4 xl:grid-cols-2">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <div><h2 className="text-sm font-medium text-slate-200">Consumption trend</h2><p className="mt-1 text-xs text-slate-500">Next 24 hours from the forecasting model</p></div>
            <span className="rounded-full border border-blue-400/15 bg-blue-400/[0.05] px-2.5 py-1 text-[11px] text-blue-300">Forecast</span>
          </div>
          {forecastState.isLoading ? <div className="h-80 animate-pulse rounded-2xl bg-card" /> : forecastState.error ? <PanelState title="Forecast unavailable" message={forecastState.error} tone="error" /> : forecastState.data?.forecast?.length ? <div className="surface rounded-2xl p-5"><ForecastChart forecast={forecastState.data.forecast} /></div> : <PanelState title="No forecast data" message="The forecast service returned no records." />}
        </div>
        <div>
          <div className="mb-3 flex items-center justify-between">
            <div><h2 className="text-sm font-medium text-slate-200">Top consuming regions</h2><p className="mt-1 text-xs text-slate-500">Ranked from the latest 100 records</p></div>
            <span className="rounded-full border border-emerald-400/15 bg-emerald-400/[0.05] px-2.5 py-1 text-[11px] text-emerald-300">Live sample</span>
          </div>
          {historyState.isLoading ? <div className="h-80 animate-pulse rounded-2xl bg-card" /> : historyState.error ? <PanelState title="History unavailable" message={historyState.error} tone="error" /> : regionalTotals.length === 0 ? <PanelState title="No regional data" message="The history service returned no records." /> : <div className="surface min-h-80 rounded-2xl p-5"><div className="space-y-5">{regionalTotals.map(([region, total], index) => <div key={region}><div className="mb-2 flex items-center justify-between text-xs"><span className="font-medium text-slate-300">{index + 1}. {region}</span><span className="text-slate-500">{numberFormatter.format(total)} kWh</span></div><div className="h-2 overflow-hidden rounded-full bg-slate-800"><div className={`h-full rounded-full bg-gradient-to-r from-blue-500 to-emerald-400 transition-all duration-700 ${regionBarWidths[index]}`} /></div></div>)}</div><p className="mt-7 border-t border-white/[0.06] pt-4 text-[11px] text-slate-600">Distribution reflects the latest records available from the History API.</p></div>}
        </div>
      </div>
    </section>
  );
}

export default DashboardPage;
