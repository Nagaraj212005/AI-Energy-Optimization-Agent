import { AlertTriangle, Database, Gauge, ShieldAlert } from 'lucide-react';
import PanelState from '../components/PanelState';
import StatCard from '../components/StatCard';
import { useAnomalies } from '../hooks/useAnomalies';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

function formatDateTime(value) {
  return new Date(value.replace(' ', 'T')).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

function signalLevel(score) {
  if (score <= -0.15) return { label: 'Critical signal', className: 'text-red-300 bg-red-400/10 border-red-400/20' };
  if (score <= -0.05) return { label: 'Elevated signal', className: 'text-amber-300 bg-amber-400/10 border-amber-400/20' };
  return { label: 'Review signal', className: 'text-blue-300 bg-blue-400/10 border-blue-400/20' };
}

function AnomalyPage() {
  const { data, isLoading, error } = useAnomalies();

  if (isLoading) {
    return (
      <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
        <div className="h-10 w-80 animate-pulse rounded-lg bg-white/[0.06]" />
        <div className="mt-3 h-4 w-96 max-w-full animate-pulse rounded bg-white/[0.04]" />
        <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{[1, 2, 3, 4].map((item) => <div key={item} className="h-36 animate-pulse rounded-2xl bg-card" />)}</div>
      </section>
    );
  }

  if (error) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="Anomaly detection unavailable" message={error} tone="error" /></section>;
  }

  const anomalies = data?.anomalies;
  if (!data || !Array.isArray(anomalies)) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="No anomaly data" message="The anomaly API returned an unexpected response." /></section>;
  }

  const criticalCount = anomalies.filter(({ anomaly_score: score }) => score <= -0.15).length;
  const elevatedCount = anomalies.filter(({ anomaly_score: score }) => score > -0.15 && score <= -0.05).length;
  const lowestScore = anomalies.length ? Math.min(...anomalies.map(({ anomaly_score: score }) => score)) : 0;
  const stats = [
    { label: 'Total anomalies', value: numberFormatter.format(data.total_anomalies), icon: ShieldAlert, accent: 'bg-red-400/10 text-red-300' },
    { label: 'Records scanned', value: numberFormatter.format(data.total_records), icon: Database, accent: 'bg-blue-400/10 text-blue-300' },
    { label: 'Critical signals', value: numberFormatter.format(criticalCount), icon: AlertTriangle, accent: 'bg-amber-400/10 text-amber-300' },
    { label: 'Lowest anomaly score', value: lowestScore.toFixed(5), icon: Gauge, accent: 'bg-cyan-400/10 text-cyan-300' },
  ];

  return (
    <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">Anomaly detection</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Spot what needs attention.</h1>
        <p className="mt-2 text-sm text-slate-500">The most unusual consumption records identified by the anomaly model.</p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => <StatCard key={stat.label} {...stat} />)}
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-red-400/15 bg-red-400/[0.04] p-5"><p className="text-xs text-red-200/70">Critical signal</p><p className="mt-3 text-2xl font-semibold text-red-200">{criticalCount}</p><p className="mt-1 text-xs text-slate-500">Score at or below -0.15</p></div>
        <div className="rounded-2xl border border-amber-400/15 bg-amber-400/[0.04] p-5"><p className="text-xs text-amber-200/70">Elevated signal</p><p className="mt-3 text-2xl font-semibold text-amber-200">{elevatedCount}</p><p className="mt-1 text-xs text-slate-500">Score between -0.15 and -0.05</p></div>
        <div className="rounded-2xl border border-blue-400/15 bg-blue-400/[0.04] p-5"><p className="text-xs text-blue-200/70">Review signal</p><p className="mt-3 text-2xl font-semibold text-blue-200">{Math.max(anomalies.length - criticalCount - elevatedCount, 0)}</p><p className="mt-1 text-xs text-slate-500">Remaining flagged records</p></div>
      </div>

      <div className="mt-8 rounded-2xl border border-white/[0.07] bg-card p-5 sm:p-6">
        <div className="mb-5 flex items-center justify-between gap-4">
          <div><h2 className="text-sm font-medium text-slate-200">Flagged records</h2><p className="mt-1 text-xs text-slate-500">Sorted by anomaly score from the detection service</p></div>
          <span className="text-xs text-slate-600">Top {anomalies.length}</span>
        </div>
        {anomalies.length === 0 ? <PanelState title="No anomalies detected" message="The model did not flag any records in the current dataset." /> : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] text-left text-sm">
              <thead className="border-b border-white/[0.06] text-xs text-slate-500"><tr><th className="pb-3 font-medium">Timestamp</th><th className="pb-3 font-medium">Region</th><th className="pb-3 font-medium">Consumption</th><th className="pb-3 font-medium">Anomaly score</th><th className="pb-3 text-right font-medium">Signal</th></tr></thead>
              <tbody className="divide-y divide-white/[0.05]">
                {anomalies.map((item) => { const level = signalLevel(item.anomaly_score); return (
                  <tr key={`${item.datetime}-${item.region}`} className="text-slate-300">
                    <td className="py-3">{formatDateTime(item.datetime)}</td>
                    <td className="py-3">{item.region}</td>
                    <td className="py-3 font-medium text-white">{numberFormatter.format(item.consumption)} <span className="text-xs font-normal text-slate-500">kWh</span></td>
                    <td className="py-3 font-mono text-xs text-red-300">{item.anomaly_score.toFixed(5)}</td>
                    <td className="py-3 text-right"><span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] ${level.className}`}><span className="h-1.5 w-1.5 rounded-full bg-current" />{level.label}</span></td>
                  </tr>
                ); })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export default AnomalyPage;
