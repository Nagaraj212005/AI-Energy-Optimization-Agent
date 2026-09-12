function PanelState({ title, message, tone = 'default' }) {
  const toneStyles = tone === 'error'
    ? 'border-red-400/20 bg-red-400/[0.04] text-red-300'
    : 'border-white/[0.07] bg-card text-slate-400';

  return (
    <div className={`flex min-h-48 flex-col items-center justify-center rounded-2xl border px-6 text-center shadow-xl shadow-slate-950/10 ${toneStyles}`}>
      <p className="text-sm font-medium">{title}</p>
      <p className="mt-2 max-w-sm text-xs leading-5 text-slate-500">{message}</p>
    </div>
  );
}

export default PanelState;
