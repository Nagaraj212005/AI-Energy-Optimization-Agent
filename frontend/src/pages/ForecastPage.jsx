import { CalendarClock, Gauge, TrendingDown, TrendingUp } from 'lucide-react';
import ForecastChart from '../components/ForecastChart';
import PanelState from '../components/PanelState';
import StatCard from '../components/StatCard';
import { useForecast } from '../hooks/useForecast';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

function formatDateTime(value) {
  return new Date(value.replace(' ', 'T')).toLocaleString([], {
    weekday: 'short',
    hour: 'numeric',
    minute: '2-digit',
  });
}

function ForecastPage() {
  const { data, isLoading, error } = useForecast();

  if (isLoading) {
    return (
      <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
        <div className="h-10 w-72 animate-pulse rounded-lg bg-white/[0.06]" />
        <div className="mt-3 h-4 w-96 max-w-full animate-pulse rounded bg-white/[0.04]" />
        <div className="mt-8 h-80 animate-pulse rounded-2xl bg-card" />
      </section>
    );
  }

  if (error) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="Forecast unavailable" message={error} tone="error" /></section>;
  }

  const forecast = data?.forecast;
  if (!Array.isArray(forecast) || forecast.length === 0) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="No forecast data" message="The forecast API returned no prediction records." /></section>;
  }

  const values = forecast.map((item) => item.predicted_consumption);
  const average = values.reduce((sum, value) => sum + value, 0) / values.length;
  const peak = Math.max(...values);
  const low = Math.min(...values);
  const peakIndex = values.indexOf(peak);
  const summary = [
    { label: 'Forecast window', value: `${forecast.length} hours`, icon: CalendarClock, accent: 'bg-blue-400/10 text-blue-300' },
    { label: 'Average prediction', value: numberFormatter.format(average), suffix: 'kWh', icon: Gauge, accent: 'bg-emerald-400/10 text-emerald-300' },
    { label: 'Peak prediction', value: numberFormatter.format(peak), suffix: 'kWh', icon: TrendingUp, accent: 'bg-amber-400/10 text-amber-300' },
    { label: 'Lowest prediction', value: numberFormatter.format(low), suffix: 'kWh', icon: TrendingDown, accent: 'bg-cyan-400/10 text-cyan-300' },
  ];

  return (
    <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">Forecast</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Plan ahead with confidence.</h1>
        <p className="mt-2 text-sm text-slate-500">Model-generated consumption predictions for the next 24 hours.</p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {summary.map((stat) => <StatCard key={stat.label} {...stat} />)}
      </div>

      <div className="mt-8 grid gap-4 xl:grid-cols-[minmax(0,1.4fr)_minmax(340px,0.6fr)]">
        <div className="rounded-2xl border border-white/[0.07] bg-card p-5 sm:p-6">
          <div className="mb-5 flex items-center justify-between gap-4">
            <div>
              <h2 className="text-sm font-medium text-slate-200">24-hour forecast</h2>
              <p className="mt-1 text-xs text-slate-500">Predicted consumption by hour</p>
            </div>
            <span className="rounded-full border border-blue-400/20 bg-blue-400/[0.06] px-3 py-1.5 text-xs text-blue-300">Live model output</span>
          </div>
          <ForecastChart forecast={forecast} />
        </div>

        <div className="rounded-2xl border border-white/[0.07] bg-card p-5 sm:p-6">
          <h2 className="text-sm font-medium text-slate-200">Forecast summary</h2>
          <p className="mt-1 text-xs text-slate-500">Highest expected demand</p>
          <p className="mt-6 text-2xl font-semibold text-white">{numberFormatter.format(peak)} <span className="text-sm font-normal text-slate-500">kWh</span></p>
          <p className="mt-2 text-xs text-slate-500">Around {formatDateTime(forecast[peakIndex].datetime)}</p>
          <div className="mt-8 border-t border-white/[0.06] pt-5">
            <p className="text-xs text-slate-500">Prediction range</p>
            <div className="mt-3 flex items-end justify-between">
              <span className="text-lg font-medium text-emerald-300">{numberFormatter.format(low)} kWh</span>
              <span className="text-xs text-slate-600">to</span>
              <span className="text-lg font-medium text-amber-300">{numberFormatter.format(peak)} kWh</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 rounded-2xl border border-white/[0.07] bg-card p-5 sm:p-6">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-medium text-slate-200">Prediction table</h2>
            <p className="mt-1 text-xs text-slate-500">Hourly values returned by the forecast service</p>
          </div>
          <span className="text-xs text-slate-600">{forecast.length} records</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[520px] text-left text-sm">
            <thead className="border-b border-white/[0.06] text-xs text-slate-500">
              <tr><th className="pb-3 font-medium">Time</th><th className="pb-3 font-medium">Predicted consumption</th><th className="pb-3 text-right font-medium">Status</th></tr>
            </thead>
            <tbody className="divide-y divide-white/[0.05]">
              {forecast.map((item, index) => (
                <tr key={item.datetime} className="text-slate-300">
                  <td className="py-3">{formatDateTime(item.datetime)}</td>
                  <td className="py-3 font-medium text-white">{numberFormatter.format(item.predicted_consumption)} <span className="text-xs font-normal text-slate-500">kWh</span></td>
                  <td className="py-3 text-right text-xs text-slate-500">{index === peakIndex ? <span className="text-amber-300">Peak window</span> : 'Forecasted'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

export default ForecastPage;
