import React, { useMemo, useState } from 'react';
import { useApi } from '../components/hooks';
import { api } from '../mock';
import { useStore } from '../store';
import { EXPENSE_CATEGORIES } from '../data';
import { fa, toman } from '../utils';
import { Icon, ProgressBar, Sk } from '../components/ui';

export function Budget() {
  const { budgets, setBudgets, toast } = useStore();
  const status = useApi(() => api.budgetStatus(), [budgets]);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  const rows = useMemo(() => {
    if (!status.data) return [];
    return status.data;
  }, [status.data]);

  const total = rows.reduce((s, b) => s + b.limit, 0);
  const spent = rows.reduce((s, b) => s + b.spent, 0);
  const remaining = Math.max(0, total - spent);

  const valueFor = (category: string, limit: number) => drafts[category] ?? String(limit);

  const save = async (category: string) => {
    const raw = drafts[category];
    if (raw == null) return;
    const limit = Number(raw.replace(/[^0-9]/g, '')) || 0;
    const next = budgets.map((b) => b.category === category ? { ...b, limit } : b);
    if (!next.some((b) => b.category === category)) next.push({ category, limit });
    setSaving(true);
    try {
      await setBudgets(next);
      setDrafts((d) => { const copy = { ...d }; delete copy[category]; return copy; });
      toast('بودجه ذخیره شد', `سقف «${category}» به‌روزرسانی شد.`);
    } finally { setSaving(false); }
  };

  const addMissing = async (category: string) => {
    if (budgets.some((b) => b.category === category)) return;
    const next = [...budgets, { category, limit: 0 }];
    await setBudgets(next);
  };

  return (
    <div style={{ maxWidth: 1180, margin: '0 auto', padding: '32px 20px 90px', animation: 'pagein .45s var(--ease) both' }}>
      <div style={{ marginBottom: 24 }}>
        <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 6 }}>مدیریت مالی</div>
        <h1 style={{ fontSize: 30, fontWeight: 600 }}>بودجه‌ی ماهانه</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: 6 }}>سقف هزینه‌ها را تنظیم کن و مصرف هر دسته را در همین صفحه ببین.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,minmax(0,1fr))', gap: 12, marginBottom: 18 }}>
        {[
          ['کل بودجه', total, 'var(--text-primary)'],
          ['مصرف‌شده', spent, spent > total ? 'var(--danger)' : 'var(--warning)'],
          ['باقی‌مانده', remaining, 'var(--success)'],
        ].map(([label, value, color]) => (
          <div key={String(label)} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 18 }}>
            <div style={{ color: 'var(--text-secondary)', fontSize: 13 }}>{label}</div>
            <div className="num" style={{ fontSize: 23, marginTop: 7, color: String(color) }}>{toman(Number(value))}</div>
          </div>
        ))}
      </div>

      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: 20 }}>
        {status.status === 'loading' && <Sk h={180} />}
        {status.status === 'error' && <div style={{ color: 'var(--danger)' }}>دریافت وضعیت بودجه ناموفق بود.</div>}
        {rows.map((b) => {
          const over = b.pct >= 100;
          return (
            <div key={b.category} style={{ padding: '14px 0', borderBottom: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>{b.category}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: 12, marginTop: 2 }}>{toman(b.spent)} از {toman(b.limit)}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <input
                    value={valueFor(b.category, b.limit).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                    onChange={(e) => setDrafts((d) => ({ ...d, [b.category]: e.target.value }))}
                    inputMode="numeric"
                    aria-label={`سقف بودجه ${b.category}`}
                    style={{ width: 145, height: 38, background: 'rgba(255,255,255,.03)', border: '1px solid var(--border-strong)', borderRadius: 'var(--radius)', padding: '0 10px', textAlign: 'left' }}
                  />
                  <button onClick={() => save(b.category)} disabled={saving} style={{ height: 38, padding: '0 12px', borderRadius: 'var(--radius)', background: 'var(--accent-blue)', color: '#fff' }}>ذخیره</button>
                </div>
              </div>
              <div style={{ marginTop: 10 }}><ProgressBar pct={b.pct} /></div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: 12, color: over ? 'var(--danger)' : b.pct >= 80 ? 'var(--warning)' : 'var(--text-tertiary)' }}>
                <span>{fa(b.pct)}٪ مصرف</span>
                {over && <span>از سقف عبور کرده</span>}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: 18 }}>
        <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 10 }}>افزودن دسته‌ی بودجه</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          {EXPENSE_CATEGORIES.filter((c) => !budgets.some((b) => b.category === c)).map((category) => (
            <button key={category} onClick={() => addMissing(category)} style={{ border: '1px solid var(--border-strong)', borderRadius: 'var(--radius)', padding: '8px 12px', color: 'var(--text-secondary)', background: 'rgba(255,255,255,.02)' }}>
              <Icon n="plus" s={14} /> {category}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
