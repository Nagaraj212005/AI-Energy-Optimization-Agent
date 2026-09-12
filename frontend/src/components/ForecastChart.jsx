import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const numberFormatter = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });

function ForecastChart({ forecast }) {
  const chartData = forecast.map((item) => ({
    ...item,
    label: new Date(item.datetime.replace(' ', 'T')).toLocaleTimeString([], { hour: 'numeric' }),
  }));

  return (
    <div className="h-[320px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 12, right: 12, left: -16, bottom: 4 }}>
          <defs>
            <linearGradient id="forecastFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.35} />
              <stop offset="100%" stopColor="#3B82F6" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 11 }} interval="preserveStartEnd" />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={(value) => numberFormatter.format(value)} width={58} />
          <Tooltip
            contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(148, 163, 184, 0.16)', borderRadius: '12px', color: '#f8fafc' }}
            labelStyle={{ color: '#94a3b8', marginBottom: '4px' }}
            formatter={(value) => [`${numberFormatter.format(value)} kWh`, 'Predicted consumption']}
          />
          <Area type="monotone" dataKey="predicted_consumption" stroke="#60A5FA" strokeWidth={2.5} fill="url(#forecastFill)" dot={false} activeDot={{ r: 5, fill: '#10B981', stroke: '#0B1220', strokeWidth: 2 }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ForecastChart;
