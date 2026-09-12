import { CircleDollarSign, ListChecks, ShieldAlert, TrendingDown } from 'lucide-react';
import PanelState from '../components/PanelState';
import RecommendationCard from '../components/RecommendationCard';
import StatCard from '../components/StatCard';
import { useRecommendations } from '../hooks/useRecommendations';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

function RecommendationsPage() {
  const { data, isLoading, error } = useRecommendations();

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
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="Recommendations unavailable" message={error} tone="error" /></section>;
  }

  const recommendations = data?.recommendations;
  if (!data || !Array.isArray(recommendations)) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="No recommendation data" message="The recommendation API returned an unexpected response." /></section>;
  }

  const totalSaving = recommendations.reduce((sum, item) => sum + item.saving, 0);
  const criticalCount = recommendations.filter((item) => item.priority === 'Critical').length;
  const averageSaving = recommendations.length ? totalSaving / recommendations.length : 0;
  const stats = [
    { label: 'Opportunities found', value: numberFormatter.format(data.total_records), icon: ListChecks, accent: 'bg-blue-400/10 text-blue-300' },
    { label: 'Total potential saving', value: numberFormatter.format(totalSaving), suffix: 'kWh', icon: CircleDollarSign, accent: 'bg-emerald-400/10 text-emerald-300' },
    { label: 'Critical priority', value: numberFormatter.format(criticalCount), icon: ShieldAlert, accent: 'bg-red-400/10 text-red-300' },
    { label: 'Average saving', value: numberFormatter.format(averageSaving), suffix: 'kWh', icon: TrendingDown, accent: 'bg-amber-400/10 text-amber-300' },
  ];

  return (
    <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">Recommendations</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Turn insight into action.</h1>
        <p className="mt-2 text-sm text-slate-500">Prioritized opportunities generated from your current energy profile.</p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => <StatCard key={stat.label} {...stat} />)}
      </div>

      <div className="mt-8 flex items-end justify-between gap-4">
        <div><h2 className="text-sm font-medium text-slate-200">Priority opportunities</h2><p className="mt-1 text-xs text-slate-500">Top model-ranked recommendations by estimated saving</p></div>
        <span className="text-xs text-slate-600">Showing {Math.min(recommendations.length, 12)} of {recommendations.length}</span>
      </div>
      {recommendations.length === 0 ? <div className="mt-4"><PanelState title="No recommendations found" message="The recommendation model did not return any opportunities for the current data." /></div> : (
        <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {recommendations.slice(0, 12).map((recommendation, index) => <RecommendationCard key={`${recommendation.datetime}-${recommendation.region}-${index}`} recommendation={recommendation} />)}
        </div>
      )}
    </section>
  );
}

export default RecommendationsPage;
