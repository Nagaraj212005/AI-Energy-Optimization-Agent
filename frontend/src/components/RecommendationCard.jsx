import { ArrowDownRight, MapPin, Zap } from 'lucide-react';

const priorityStyles = {
  Critical: 'border-red-400/20 bg-red-400/10 text-red-300',
  High: 'border-amber-400/20 bg-amber-400/10 text-amber-300',
  Medium: 'border-blue-400/20 bg-blue-400/10 text-blue-300',
  Low: 'border-slate-400/20 bg-slate-400/10 text-slate-300',
};

function RecommendationCard({ recommendation }) {
  const {
    region,
    priority,
    saving,
    saving_percent: savingPercent,
    current_consumption: current,
    recommended_consumption: recommended,
    recommendation: message,
  } = recommendation;

  return (
    <article className="flex flex-col rounded-2xl border border-white/[0.07] bg-card p-5 shadow-2xl shadow-slate-950/10 transition hover:border-white/[0.13]">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 text-xs text-slate-400"><MapPin size={14} className="text-secondary" />{region}</div>
        <span className={`rounded-full border px-2.5 py-1 text-[11px] font-medium ${priorityStyles[priority] || priorityStyles.Low}`}>{priority}</span>
      </div>
      <div className="mt-5 flex items-end justify-between gap-4">
        <div><p className="text-xs text-slate-500">Potential saving</p><p className="mt-1 text-2xl font-semibold text-emerald-300">{saving.toLocaleString()} <span className="text-xs font-normal text-slate-500">kWh</span></p></div>
        <div className="flex items-center gap-1 text-xs text-emerald-300"><ArrowDownRight size={14} />{savingPercent.toFixed(2)}%</div>
      </div>
      <p className="mt-5 flex-1 border-t border-white/[0.06] pt-4 text-sm leading-6 text-slate-400">{message}</p>
      <div className="mt-5 grid grid-cols-2 gap-3 border-t border-white/[0.06] pt-4 text-xs">
        <div><p className="text-slate-600">Current</p><p className="mt-1 font-medium text-slate-300">{current.toLocaleString()} kWh</p></div>
        <div><p className="text-slate-600">Recommended</p><p className="mt-1 font-medium text-white">{recommended.toLocaleString()} kWh</p></div>
      </div>
      <div className="mt-4 flex items-center gap-1.5 text-[11px] text-slate-600"><Zap size={13} />Model-ranked opportunity</div>
    </article>
  );
}

export default RecommendationCard;
