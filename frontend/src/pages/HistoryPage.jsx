import { ChevronLeft, ChevronRight, Download, Filter, Search } from 'lucide-react';
import { useMemo, useState } from 'react';
import PanelState from '../components/PanelState';
import { useHistory } from '../hooks/useHistory';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
const pageSize = 10;

function formatDateTime(value) {
  return new Date(value.replace(' ', 'T')).toLocaleString([], { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
}

function HistoryPage() {
  const { data, isLoading, error } = useHistory();
  const [search, setSearch] = useState('');
  const [region, setRegion] = useState('all');
  const [page, setPage] = useState(1);

  const rows = data?.history || [];
  const regions = useMemo(() => [...new Set(rows.map((row) => row.region))].sort(), [rows]);
  const filteredRows = useMemo(() => rows.filter((row) => {
    const matchesSearch = `${row.region} ${row.datetime}`.toLowerCase().includes(search.toLowerCase());
    return matchesSearch && (region === 'all' || row.region === region);
  }), [rows, search, region]);
  const pageCount = Math.max(1, Math.ceil(filteredRows.length / pageSize));
  const visibleRows = filteredRows.slice((page - 1) * pageSize, page * pageSize);

  function updateSearch(value) { setSearch(value); setPage(1); }
  function updateRegion(value) { setRegion(value); setPage(1); }

  function exportCsv() {
    const header = 'datetime,region,consumption';
    const body = rows.map((row) => `${row.datetime},${row.region},${row.consumption}`).join('\n');
    const blob = new Blob([`${header}\n${body}`], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'energy-history.csv';
    link.click();
    URL.revokeObjectURL(url);
  }

  if (isLoading) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><div className="h-10 w-72 animate-pulse rounded-lg bg-white/[0.06]" /><div className="mt-3 h-4 w-96 max-w-full animate-pulse rounded bg-white/[0.04]" /><div className="mt-8 h-[460px] animate-pulse rounded-2xl bg-card" /></section>;
  }
  if (error) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="History unavailable" message={error} tone="error" /></section>;
  }
  if (!data || !Array.isArray(data.history)) {
    return <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8"><PanelState title="No history data" message="The history API returned an unexpected response." /></section>;
  }

  return (
    <section className="mx-auto w-full max-w-[1400px] px-5 py-8 sm:px-8">
      <div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-secondary">History</p><h1 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Explore your energy story.</h1><p className="mt-2 text-sm text-slate-500">Review the latest consumption records returned by the data service.</p></div>
      <div className="mt-8 rounded-2xl border border-white/[0.07] bg-card p-5 sm:p-6">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div className="relative flex-1 lg:max-w-sm"><Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600" /><input value={search} onChange={(event) => updateSearch(event.target.value)} placeholder="Search region or timestamp" className="h-10 w-full rounded-xl border border-white/[0.08] bg-white/[0.025] pl-9 pr-3 text-sm text-slate-200 outline-none transition placeholder:text-slate-600 focus:border-primary/50" /></div>
          <div className="flex flex-wrap items-center gap-2"><Filter size={15} className="text-slate-600" /><select value={region} onChange={(event) => updateRegion(event.target.value)} className="h-10 rounded-xl border border-white/[0.08] bg-[#151f32] px-3 text-sm text-slate-300 outline-none focus:border-primary/50"><option value="all">All regions</option>{regions.map((item) => <option key={item} value={item}>{item}</option>)}</select><span className="text-xs text-slate-600">{filteredRows.length} records</span><button type="button" onClick={exportCsv} className="flex h-10 items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.035] px-3 text-xs text-slate-300 transition hover:bg-white/[0.08] hover:text-white"><Download size={14} />Export CSV</button></div>
        </div>
        <div className="mt-6 overflow-x-auto">
          {visibleRows.length === 0 ? <PanelState title="No matching records" message="Try a different search or region filter." /> : <table className="w-full min-w-[600px] text-left text-sm"><thead className="border-b border-white/[0.06] text-xs text-slate-500"><tr><th className="pb-3 font-medium">Timestamp</th><th className="pb-3 font-medium">Region</th><th className="pb-3 text-right font-medium">Consumption</th></tr></thead><tbody className="divide-y divide-white/[0.05]">{visibleRows.map((row) => <tr key={`${row.datetime}-${row.region}`} className="text-slate-300"><td className="py-3.5">{formatDateTime(row.datetime)}</td><td className="py-3.5">{row.region}</td><td className="py-3.5 text-right font-medium text-white">{numberFormatter.format(row.consumption)} <span className="text-xs font-normal text-slate-500">kWh</span></td></tr>)}</tbody></table>}
        </div>
        <div className="mt-5 flex items-center justify-between border-t border-white/[0.06] pt-4"><span className="text-xs text-slate-600">Page {page} of {pageCount}</span><div className="flex items-center gap-2"><button type="button" aria-label="Previous page" disabled={page === 1} onClick={() => setPage((current) => current - 1)} className="rounded-lg border border-white/[0.08] p-2 text-slate-400 transition hover:bg-white/[0.05] hover:text-white disabled:cursor-not-allowed disabled:opacity-30"><ChevronLeft size={16} /></button><button type="button" aria-label="Next page" disabled={page >= pageCount} onClick={() => setPage((current) => current + 1)} className="rounded-lg border border-white/[0.08] p-2 text-slate-400 transition hover:bg-white/[0.05] hover:text-white disabled:cursor-not-allowed disabled:opacity-30"><ChevronRight size={16} /></button></div></div>
      </div>
    </section>
  );
}

export default HistoryPage;
