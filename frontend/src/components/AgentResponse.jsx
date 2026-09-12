import { Bot, ChevronRight } from 'lucide-react';

function AgentResponse({ response }) {
  const title = response.module || response.message || 'Assistant response';
  const payload = response.data || response;

  return (
    <div className="max-w-2xl rounded-2xl rounded-tl-md border border-white/[0.07] bg-card p-4 shadow-xl shadow-slate-950/10">
      <div className="flex items-center gap-2 text-xs font-medium text-secondary"><Bot size={15} />{title}</div>
      {response.supported_queries ? (
        <div className="mt-4 space-y-3 text-sm text-slate-400">
          <p>I can help with these workspace areas:</p>
          <div className="flex flex-wrap gap-2">{response.supported_queries.map((item) => <span key={item} className="rounded-full border border-white/[0.08] px-2.5 py-1 text-xs text-slate-300">{item}</span>)}</div>
        </div>
      ) : (
        <details className="group mt-4" open>
          <summary className="flex cursor-pointer list-none items-center gap-1 text-xs text-slate-500 transition hover:text-slate-300"><ChevronRight size={14} className="transition group-open:rotate-90" />View returned data</summary>
          <pre className="mt-3 max-h-72 overflow-auto rounded-xl border border-white/[0.06] bg-slate-950/50 p-3 text-[11px] leading-5 text-slate-400">{JSON.stringify(payload, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}

export default AgentResponse;
