import { NavLink } from 'react-router-dom';
import { Activity, CircleHelp, X } from 'lucide-react';
import { navigationItems } from '../utils/navigation';

function Sidebar({ isOpen, onClose }) {
  return (
    <>
      <button
        type="button"
        aria-label="Close navigation"
        className={`fixed inset-0 z-30 bg-slate-950/70 transition-opacity lg:hidden ${
          isOpen ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
        onClick={onClose}
      />
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-[264px] flex-col border-r border-white/[0.07] bg-[#0d1526]/95 px-3 py-5 shadow-2xl shadow-slate-950/20 backdrop-blur-xl transition-transform duration-300 lg:static lg:z-auto lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-3">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-[14px] bg-gradient-to-br from-blue-400/20 to-emerald-400/10 text-blue-300 ring-1 ring-blue-300/30">
              <Activity size={19} strokeWidth={2.5} />
            </div>
            <div>
              <p className="text-[13px] font-semibold tracking-tight text-white">Energize</p>
              <p className="mt-0.5 text-[10px] text-slate-500">Optimization intelligence</p>
            </div>
          </div>
          <button
            type="button"
            aria-label="Close navigation"
            className="rounded-lg p-2 text-slate-500 transition hover:bg-white/[0.06] hover:text-white lg:hidden"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>

        <nav className="mt-9 flex-1 space-y-1" aria-label="Main navigation">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600">
            Workspace
          </p>
          {navigationItems.map(({ label, path, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              end={path === '/'}
              onClick={onClose}
              className={({ isActive }) =>
                `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition ${
                  isActive
                    ? 'bg-blue-400/[0.11] font-medium text-blue-200 ring-1 ring-blue-300/25 shadow-lg shadow-blue-950/10'
                    : 'text-slate-400 hover:bg-white/[0.05] hover:text-slate-100'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon size={17} className={isActive ? 'text-primary' : 'text-slate-500 group-hover:text-slate-300'} />
                  <span>{label}</span>
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="rounded-2xl border border-emerald-300/10 bg-emerald-300/[0.035] p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-300">Agent status</span>
            <span className="flex items-center gap-1.5 text-[11px] text-emerald-400">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Online
            </span>
          </div>
          <p className="mt-2 text-[11px] leading-relaxed text-slate-500">
            Monitoring your energy network in real time.
          </p>
        </div>
        <div className="mt-4 flex items-center justify-between px-3 text-[11px] text-slate-600">
          <span>v0.1.0</span>
          <CircleHelp size={13} />
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
