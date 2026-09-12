import { Bell, Menu, Moon, Search, Wifi } from 'lucide-react';

function Navbar({ onMenuClick }) {
  return (
    <header className="sticky top-0 z-20 flex h-[72px] shrink-0 items-center justify-between border-b border-white/[0.07] bg-[#0b1220]/80 px-5 backdrop-blur-xl sm:px-8">
      <div className="flex items-center gap-3">
        <button
          type="button"
          aria-label="Open navigation"
          className="rounded-xl p-2 text-slate-400 transition hover:bg-white/[0.06] hover:text-white lg:hidden"
          onClick={onMenuClick}
        >
          <Menu size={20} />
        </button>
        <div className="hidden items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.035] px-3 py-2 text-sm text-slate-500 shadow-inner shadow-white/[0.02] sm:flex sm:w-72">
          <Search size={16} />
          <span>Search workspace</span>
          <kbd className="ml-auto rounded border border-white/[0.08] px-1.5 py-0.5 text-[10px] text-slate-600">⌘ K</kbd>
        </div>
        <p className="text-sm font-medium text-slate-300 sm:hidden">Workspace</p>
      </div>

      <div className="flex items-center gap-1 sm:gap-2">
        <div className="mr-1 hidden items-center gap-1.5 rounded-full border border-emerald-400/15 bg-emerald-400/[0.05] px-2.5 py-1.5 text-[11px] text-emerald-300 md:flex"><Wifi size={13} /> Live</div>
        <button type="button" aria-label="Toggle dark mode" className="rounded-xl p-2.5 text-slate-400 transition hover:bg-white/[0.06] hover:text-white">
          <Moon size={18} />
        </button>
        <button type="button" aria-label="View notifications" className="relative rounded-xl p-2.5 text-slate-400 transition hover:bg-white/[0.06] hover:text-white">
          <Bell size={18} />
          <span className="absolute right-2.5 top-2.5 h-1.5 w-1.5 rounded-full bg-secondary ring-2 ring-[#0B1220]" />
        </button>
        <div className="ml-1 flex h-9 w-9 items-center justify-center rounded-full border border-white/20 bg-gradient-to-br from-blue-400 to-emerald-400 text-[11px] font-bold text-slate-950 shadow-lg shadow-blue-950/20">
          AR
        </div>
      </div>
    </header>
  );
}

export default Navbar;
