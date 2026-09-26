import React, { useMemo, useState } from 'react';
import { useApi } from '../components/hooks';
import { api } from '../mock';
import { fa, toman, short } from '../utils';
import { Seg, ProgressBar, Sk } from '../components/ui';
import { getCategoryColor } from '../data';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

const TOOLTIP_STYLE = {
  background: '#11151d',
  border: '1px solid rgba(255,255,255,.12)',
  borderRadius: 10,
  color: '#f4f6fa',
  boxShadow: '0 16px 40px rgba(0,0,0,.28)',
};

export function Analytics() {
  const [range, setRange] = useState('30d');
  const series = useApi(() => api.series(range), [range]);
  const cats = useApi(() => api.categories(range), [range]);
  const insights = useApi(() => api.insights(range), [range]);
  const predictions = useApi(() => api.prediction(range), [range]);

  const chartData = useMemo(
    () => (series.data || []).map((x) => ({ ...x, label: x.label || x.rangeLabel })),
    [series.data],
  );
  const maxCat = useMemo(
    () => Math.max(1, ...(cats.data || []).map((x) => x.amount)),
    [cats.data],
  );

  return (
    <div style={{ maxWidth: 1180, margin: '0 auto', padding: '32px 20px 90px', animation: 'pagein .45s var(--ease) both' }}>
      <div style={{ display: 'flex', alignItems: 'end', justifyContent: 'space-between', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <div>
          <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 6 }}>مرکز بینش</div>
          <h1 style={{ fontSize: 30, fontWeight: 700 }}>تحلیل مالی</h1>
        </div>
        <Seg value={range} onChange={setRange} options={[['7d','۷ روز'],['30d','۳۰ روز'],['90d','۹۰ روز'],['1y','یک سال']]} />
      </div>

      <section style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 20, marginBottom: 14, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 12 }}>
          <div style={{ fontWeight: 600 }}>روند درآمد و هزینه</div>
          {series.status === 'loading' && series.data && (
            <span style={{ color: 'var(--text-tertiary)', fontSize: 11 }}>در حال به‌روزرسانی…</span>
          )}
        </div>

        {!series.data && series.status === 'loading' ? (
          <Sk h={300} />
        ) : (
          <div className="chart-wrap" style={{ height: 300, minWidth: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
                <CartesianGrid stroke="rgba(255,255,255,.07)" strokeDasharray="3 6" vertical={false} />
                <XAxis
                  dataKey="label"
                  tick={{ fill: '#7e8798', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  minTickGap={18}
                />
                <YAxis
                  tick={{ fill: '#7e8798', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  width={46}
                  tickFormatter={(value) => short(Number(value))}
                />
                <Tooltip
                  contentStyle={TOOLTIP_STYLE}
                  labelStyle={{ color: '#aeb6c5', marginBottom: 4 }}
                  formatter={(value, name) => [toman(Number(value)), name === 'income' ? 'درآمد' : 'هزینه']}
                />
                <Legend
                  formatter={(value) => value === 'income' ? 'درآمد' : 'هزینه'}
                  wrapperStyle={{ fontSize: 12, color: '#9ca5b4', paddingTop: 10 }}
                />
                <Line
                  name="income"
                  type="monotone"
                  dataKey="income"
                  stroke="#3ddc97"
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{ r: 4, strokeWidth: 0 }}
                  isAnimationActive
                  animationDuration={520}
                  animationEasing="ease-in-out"
                />
                <Line
                  name="expenses"
                  type="monotone"
                  dataKey="expenses"
                  stroke="#2f6bff"
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{ r: 4, strokeWidth: 0 }}
                  isAnimationActive
                  animationDuration={620}
                  animationEasing="ease-in-out"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </section>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }} className="analytics-grid">
        <section style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 20 }}>
          <div style={{ fontWeight: 600, marginBottom: 14 }}>دسته‌های هزینه</div>
          {cats.status === 'loading' && !cats.data ? <Sk h={180} /> : (cats.data || []).slice(0, 8).map((c) => (
            <div key={c.category} style={{ marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 5 }}><span>{c.category}</span><span className="num">{toman(c.amount)}</span></div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: 8, alignItems: 'center' }}><ProgressBar pct={(c.amount / maxCat) * 100} color={getCategoryColor(c.category)} /><span style={{ color: 'var(--text-secondary)', fontSize: 12 }}>{fa(c.share)}٪</span></div>
            </div>
          ))}
        </section>

        <section style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 20 }}>
          <div style={{ fontWeight: 600, marginBottom: 14 }}>بینش‌ها</div>
          {insights.status === 'loading' && !insights.data ? <Sk h={180} /> : <div style={{ display: 'grid', gap: 10 }}>{(insights.data || []).map((i) => <div key={i.id} style={{ padding: '11px 12px', borderRadius: 'var(--radius)', background: 'rgba(255,255,255,.025)', border: '1px solid var(--border)', color: i.type === 'warning' ? 'var(--warning)' : i.type === 'success' ? 'var(--success)' : 'var(--text-secondary)', fontSize: 13 }}>{i.text}</div>)}</div>}
        </section>
      </div>

      <section style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 20, marginTop: 14 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}><div style={{ fontWeight: 600 }}>پیش‌بینی سه ماه آینده</div><span style={{ color: 'var(--text-secondary)', fontSize: 12 }}>بر اساس روند فعلی</span></div>
        {predictions.status === 'loading' && !predictions.data ? <Sk h={100} /> : <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10 }} className="prediction-grid">{(predictions.data || []).map((p) => <div key={p.label} style={{ padding: 14, border: '1px solid var(--border)', borderRadius: 'var(--radius)' }}><div style={{ color: 'var(--text-secondary)', fontSize: 12 }}>{p.label}</div><div className="num" style={{ marginTop: 8 }}>هزینه: {short(p.expenses)}</div><div className="num" style={{ color: 'var(--success)', marginTop: 5 }}>درآمد: {short(p.income)}</div></div>)}</div>}
      </section>
    </div>
  );
}
