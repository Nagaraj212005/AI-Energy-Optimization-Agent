import { motion } from 'framer-motion';

function StatCard({ label, value, suffix, icon: Icon, accent, trend }) {
  return (
    <motion.article
      whileHover={{ y: -3 }}
      transition={{ duration: 0.2 }}
      className="surface rounded-2xl p-5"
    >
      <div className="flex items-start justify-between gap-4">
        <p className="text-[13px] text-slate-400">{label}</p>
        <div className={`rounded-xl p-2.5 ${accent}`}>
          <Icon size={18} />
        </div>
      </div>
      <p className="mt-6 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
        {value}
        {suffix && <span className="ml-1 text-sm font-normal text-slate-500">{suffix}</span>}
      </p>
      {trend && <p className={`mt-2 text-[11px] ${trend.startsWith('-') ? 'text-rose-300' : 'text-emerald-300'}`}>{trend} <span className="text-slate-600">vs. previous period</span></p>}
    </motion.article>
  );
}

export default StatCard;
