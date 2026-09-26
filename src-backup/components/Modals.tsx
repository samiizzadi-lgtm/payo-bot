import React, { useState } from 'react';
import {
  Transaction,
  EXPENSE_CATEGORIES,
  INCOME_CATEGORIES,
  getCategoryColor,
  suggestCategory,
} from '../data';
import {
  fa,
  toman,
  iso,
  today0,
  addDays,
  toLatin,
  dateLabel,
  fullDate,
} from '../utils';
import { Icon, Modal } from './ui';
import { useStore } from '../store';

/* ── Add transaction modal ── */
export function AddModal({
  defaults,
  onClose,
}: {
  defaults: { type?: 'income' | 'expense' };
  onClose: () => void;
}) {
  const { addTx, toast } = useStore();

  const [type, setType] = useState<'income' | 'expense'>(
    defaults.type || 'expense',
  );
  const [raw, setRaw] = useState('');
  const [cat, setCat] = useState('');
  const [name, setName] = useState('');
  const [date, setDate] = useState(iso(today0()));
  const [err, setErr] = useState<Record<string, string>>({});
  const [phase, setPhase] = useState<'form' | 'saving' | 'done'>('form');
  const [saved, setSaved] = useState<Transaction | null>(null);
  const [suggestedCat, setSuggestedCat] = useState<string | null>(null);

  const amount = Number(toLatin(raw).replace(/\D/g, '')) || 0;
  const cats = type === 'expense'
    ? EXPENSE_CATEGORIES
    : INCOME_CATEGORIES;
  const today = today0();

  const handleNameInput = (value: string) => {
    setName(value);
    const suggestion = suggestCategory(value);

    if (suggestion && cats.includes(suggestion)) {
      setSuggestedCat(suggestion);
    } else {
      setSuggestedCat(null);
    }
  };

  const inputStyle: React.CSSProperties = {
    height: 42,
    background: 'rgba(255,255,255,0.03)',
    border: '1px solid var(--border-strong)',
    borderRadius: 'var(--radius)',
    padding: '0 14px',
    color: 'var(--text-primary)',
    width: '100%',
    fontFamily: 'inherit',
    fontSize: 14,
    outline: 'none',
    transition: 'border-color 0.15s, box-shadow 0.15s',
  };

  const save = async (close: () => void) => {
    const errors: Record<string, string> = {};

    if (amount <= 0) errors.amount = 'مبلغ را وارد کن.';
    if (!cat) errors.cat = 'یک دسته انتخاب کن.';
    if (!date) errors.date = 'تاریخ را انتخاب کن.';

    setErr(errors);

    if (Object.keys(errors).length > 0) return;

    setPhase('saving');

    try {
      const transaction = await addTx({
        type,
        amount,
        category: cat,
        name,
        date,
      });

      setSaved(transaction);
      setPhase('done');

      toast(
        'تراکنش ثبت شد',
        `${toman(transaction.amount)} · ${transaction.category} · ${dateLabel(transaction.date)}`,
      );

      // بستن مودال فقط با اقدام کاربر انجام می‌شود.
      // از setTimeout برای جلوگیری از بسته‌شدن ناخواسته استفاده نمی‌کنیم.
    } catch {
      setPhase('form');
      setErr({ form: 'ثبت انجام نشد. دوباره تلاش کن.' });
    }
  };

  return (
    <Modal title={phase === 'done' ? '' : 'ثبت تراکنش'} onClose={onClose}>
      {(close) =>
        phase === 'done' && saved ? (
          <div style={{ textAlign: 'center', padding: '14px 0 6px' }}>
            <div
              style={{
                width: 64,
                height: 64,
                margin: '0 auto 14px',
                borderRadius: '50%',
                display: 'grid',
                placeItems: 'center',
                border: '1px solid rgba(61,220,151,0.5)',
                background: 'rgba(61,220,151,0.08)',
                animation: 'pop 0.4s cubic-bezier(0.2,0.7,0.2,1) both',
              }}
            >
              <svg
                width="30"
                height="30"
                viewBox="0 0 24 24"
                fill="none"
                stroke="var(--success)"
                strokeWidth={2.4}
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path
                  pathLength={1}
                  d="M5 12.5l4.5 4.5L19 7"
                  style={{
                    strokeDasharray: 1,
                    strokeDashoffset: 1,
                    animation: 'draw 0.5s ease 0.15s forwards',
                  }}
                />
              </svg>
            </div>

            <h3 style={{ fontSize: 18, fontWeight: 600 }}>
              تراکنش ثبت شد
            </h3>

            <div
              style={{
                fontSize: 30,
                margin: '10px 0 4px',
                fontFamily: 'var(--font-mono,monospace)',
                fontWeight: 500,
              }}
            >
              {saved.type === 'income' ? '+' : '−'}
              {fa(saved.amount)}
              <span
                style={{
                  fontSize: 14,
                  color: 'var(--text-secondary)',
                  fontWeight: 400,
                }}
              >
                {' '}تومان
              </span>
            </div>

            <div style={{ color: 'var(--text-secondary)' }}>
              {saved.category} · {dateLabel(saved.date)}
            </div>

            <button
              type="button"
              onClick={close}
              style={{
                marginTop: 20,
                width: '100%',
                height: 42,
                borderRadius: 'var(--radius)',
                background: 'var(--accent-blue)',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
                fontFamily: 'inherit',
                fontSize: 14,
              }}
            >
              بستن
            </button>
          </div>
        ) : (
          <div>
            {/* Type switcher */}
            <div
              style={{
                display: 'flex',
                padding: 3,
                border: '1px solid var(--border)',
                borderRadius: 8,
                background: 'rgba(255,255,255,0.02)',
                gap: 2,
                marginBottom: 16,
              }}
            >
              {([
                ['expense', 'هزینه'],
                ['income', 'درآمد'],
              ] as const).map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => {
                    setType(value);
                    setCat('');
                    setSuggestedCat(null);
                  }}
                  style={{
                    flex: 1,
                    height: 34,
                    borderRadius: 6,
                    fontSize: 14,
                    color: type === value
                      ? 'var(--text-primary)'
                      : 'var(--text-secondary)',
                    background: type === value
                      ? 'var(--surface-hover)'
                      : 'none',
                    border: type === value
                      ? '1px solid var(--border-strong)'
                      : '1px solid transparent',
                    cursor: 'pointer',
                    fontFamily: 'inherit',
                    fontWeight: type === value ? 500 : 400,
                  }}
                >
                  {label}
                </button>
              ))}
            </div>

            {/* Amount */}
            <div
              style={{
                display: 'flex',
                alignItems: 'baseline',
                gap: 10,
                borderBottom: '1px solid var(--border-strong)',
                padding: '6px 0 10px',
                margin: '0 0 12px',
              }}
            >
              <input
                inputMode="numeric"
                placeholder="۰"
                value={raw ? fa(amount) : ''}
                onChange={(event) => setRaw(event.target.value)}
                aria-label="مبلغ"
                style={{
                  flex: 1,
                  minWidth: 0,
                  background: 'none',
                  border: 0,
                  outline: 0,
                  fontSize: 40,
                  fontWeight: 500,
                  direction: 'ltr',
                  textAlign: 'right',
                  letterSpacing: '-0.02em',
                  color: 'var(--text-primary)',
                  fontFamily: 'inherit',
                }}
              />
              <span style={{ color: 'var(--text-secondary)' }}>
                تومان
              </span>
            </div>

            {err.amount && (
              <div
                style={{
                  color: 'var(--danger)',
                  fontSize: 12.5,
                  marginTop: -6,
                  marginBottom: 8,
                }}
              >
                {err.amount}
              </div>
            )}

            {/* Quick amounts */}
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 8,
                marginBottom: 20,
              }}
            >
              {[100000, 500000, 1000000, 5000000].map((value) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setRaw(String(value))}
                  style={{
                    height: 34,
                    padding: '0 13px',
                    borderRadius: 6,
                    border: '1px solid var(--border-strong)',
                    fontSize: 13,
                    color: 'var(--text-secondary)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    background: 'none',
                    fontFamily: 'inherit',
                    transition: 'all 0.15s',
                  }}
                >
                  {fa(value)}
                </button>
              ))}
            </div>

            {/* Category */}
            <div style={{ marginBottom: 18 }}>
              <div
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  marginBottom: 8,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <span>دسته</span>

                {suggestedCat && !cat && (
                  <button
                    type="button"
                    onClick={() => setCat(suggestedCat)}
                    style={{
                      fontSize: 12,
                      color: 'var(--accent-blue)',
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      fontFamily: 'inherit',
                    }}
                  >
                    پیشنهاد: {suggestedCat}
                  </button>
                )}
              </div>

              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: 8,
                }}
              >
                {cats.map((category) => (
                  <button
                    key={category}
                    type="button"
                    onClick={() => setCat(category)}
                    style={{
                      height: 34,
                      padding: '0 13px',
                      borderRadius: 6,
                      border: cat === category
                        ? '1px solid var(--accent-blue)'
                        : '1px solid var(--border-strong)',
                      fontSize: 13,
                      color: cat === category
                        ? 'var(--text-primary)'
                        : 'var(--text-secondary)',
                      background: cat === category
                        ? 'var(--accent-soft)'
                        : 'none',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 7,
                      cursor: 'pointer',
                      fontFamily: 'inherit',
                      transition: 'all 0.15s',
                    }}
                  >
                    <i
                      style={{
                        width: 7,
                        height: 7,
                        borderRadius: 2,
                        background: getCategoryColor(category),
                        display: 'inline-block',
                        flexShrink: 0,
                      }}
                    />
                    {category}
                  </button>
                ))}
              </div>

              {err.cat && (
                <div
                  style={{
                    color: 'var(--danger)',
                    fontSize: 12.5,
                    marginTop: 6,
                  }}
                >
                  {err.cat}
                </div>
              )}
            </div>

            {/* Name */}
            <div style={{ marginBottom: 18 }}>
              <label
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  display: 'block',
                  marginBottom: 6,
                }}
              >
                توضیحات (اختیاری)
              </label>

              <input
                style={inputStyle}
                placeholder={
                  type === 'expense'
                    ? 'مثلاً ناهار با دوستان'
                    : 'مثلاً پروژه‌ی طراحی'
                }
                value={name}
                onChange={(event) => handleNameInput(event.target.value)}
                onFocus={(event) => {
                  event.currentTarget.style.borderColor =
                    'var(--accent-blue)';
                  event.currentTarget.style.boxShadow =
                    '0 0 0 3px var(--accent-soft)';
                }}
                onBlur={(event) => {
                  event.currentTarget.style.borderColor = '';
                  event.currentTarget.style.boxShadow = '';
                }}
              />
            </div>

            {/* Date */}
            <div style={{ marginBottom: 22 }}>
              <label
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  display: 'block',
                  marginBottom: 8,
                }}
              >
                تاریخ · {date ? fullDate(date) : ''}
              </label>

              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: 8,
                }}
              >
                {([
                  [0, 'امروز'],
                  [1, 'دیروز'],
                  [2, 'دو روز پیش'],
                ] as [number, string][]).map(([offset, label]) => {
                  const quickDate = iso(addDays(today, -offset));

                  return (
                    <button
                      key={offset}
                      type="button"
                      onClick={() => setDate(quickDate)}
                      style={{
                        height: 34,
                        padding: '0 13px',
                        borderRadius: 6,
                        border: date === quickDate
                          ? '1px solid var(--accent-blue)'
                          : '1px solid var(--border-strong)',
                        fontSize: 13,
                        color: date === quickDate
                          ? 'var(--text-primary)'
                          : 'var(--text-secondary)',
                        background: date === quickDate
                          ? 'var(--accent-soft)'
                          : 'none',
                        cursor: 'pointer',
                        fontFamily: 'inherit',
                      }}
                    >
                      {label}
                    </button>
                  );
                })}

                <input
                  type="date"
                  style={{
                    ...inputStyle,
                    width: 'auto',
                    height: 34,
                    padding: '0 10px',
                  }}
                  value={date}
                  max={iso(today)}
                  onChange={(event) => setDate(event.target.value)}
                  aria-label="تاریخ"
                />
              </div>

              {err.date && (
                <div
                  style={{
                    color: 'var(--danger)',
                    fontSize: 12.5,
                    marginTop: 6,
                  }}
                >
                  {err.date}
                </div>
              )}
            </div>

            {err.form && (
              <div
                style={{
                  color: 'var(--danger)',
                  fontSize: 12.5,
                  marginBottom: 10,
                }}
              >
                {err.form}
              </div>
            )}

            <button
              type="button"
              disabled={phase === 'saving'}
              onClick={() => save(close)}
              style={{
                width: '100%',
                height: 44,
                borderRadius: 'var(--radius)',
                fontWeight: 500,
                fontSize: 14,
                background: 'var(--accent-blue)',
                color: '#fff',
                border: 'none',
                cursor: phase === 'saving' ? 'not-allowed' : 'pointer',
                opacity: phase === 'saving' ? 0.6 : 1,
                fontFamily: 'inherit',
                transition: 'opacity 0.15s',
              }}
            >
              {phase === 'saving'
                ? 'در حال ذخیره...'
                : 'ذخیره‌ی تراکنش'}
            </button>
          </div>
        )
      }
    </Modal>
  );
}

/* ── Transaction detail modal ── */
export function DetailModal({
  t,
  onClose,
}: {
  t: Transaction;
  onClose: () => void;
}) {
  const { removeTx, toast } = useStore();
  const [sure, setSure] = useState(false);
  const [busy, setBusy] = useState(false);

  const isIncome = t.type === 'income';

  const rows: [string, React.ReactNode][] = [
    ['نوع', isIncome ? 'درآمد' : 'هزینه'],
    ['دسته', t.category],
    ['تاریخ', fullDate(t.date)],
    [
      'وضعیت',
      t.status === 'pending'
        ? <span style={{ color: 'var(--warning)' }}>در انتظار</span>
        : 'انجام‌شده',
    ],
    [
      'منبع',
      t.source === 'telegram'
        ? 'ثبت‌شده از ربات'
        : 'ثبت‌شده در برنامه',
    ],
  ];

  const handleDelete = async () => {
    if (!sure) {
      setSure(true);
      return;
    }

    if (busy) return;

    setBusy(true);

    try {
      await removeTx(t.id);
      toast('تراکنش حذف شد', t.name, 'info');
      onClose();
    } catch {
      toast('حذف انجام نشد', 'دوباره تلاش کن.', 'info');
      setBusy(false);
    }
  };

  return (
    <Modal title={t.name || 'جزئیات تراکنش'} onClose={onClose}>
      {(close) => (
        <div>
          <div
            style={{
              fontSize: 32,
              fontWeight: 500,
              color: isIncome
                ? 'var(--success)'
                : 'var(--text-primary)',
              marginBottom: 14,
              fontFamily: 'var(--font-mono,monospace)',
            }}
          >
            {isIncome ? '+' : '−'}
            {fa(t.amount)}
            <span
              style={{
                fontSize: 14,
                color: 'var(--text-secondary)',
                fontWeight: 400,
              }}
            >
              {' '}تومان
            </span>
          </div>

          {rows.map(([label, value]) => (
            <div
              key={label}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '11px 0',
                borderBottom: '1px solid var(--border)',
                fontSize: 14,
              }}
            >
              <span style={{ color: 'var(--text-secondary)' }}>
                {label}
              </span>
              <span>{value}</span>
            </div>
          ))}

          <div
            style={{
              display: 'flex',
              gap: 10,
              marginTop: 20,
            }}
          >
            <button
              type="button"
              disabled={busy}
              onClick={handleDelete}
              style={{
                flex: 1,
                height: 42,
                borderRadius: 'var(--radius)',
                fontSize: 14,
                fontWeight: 500,
                border: '1px solid rgba(255,93,108,0.4)',
                color: 'var(--danger)',
                background: sure
                  ? 'rgba(255,93,108,0.08)'
                  : 'none',
                cursor: busy ? 'not-allowed' : 'pointer',
                fontFamily: 'inherit',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 8,
                opacity: busy ? 0.6 : 1,
              }}
            >
              <Icon n="trash" s={17} />
              {busy
                ? 'در حال حذف...'
                : sure
                  ? 'حذف نهایی'
                  : 'حذف تراکنش'}
            </button>

            <button
              type="button"
              onClick={close}
              style={{
                flex: 1,
                height: 42,
                borderRadius: 'var(--radius)',
                fontSize: 14,
                border: '1px solid var(--border-strong)',
                background: 'rgba(255,255,255,.02)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                fontFamily: 'inherit',
              }}
            >
              بستن
            </button>
          </div>
        </div>
      )}
    </Modal>
  );
}
