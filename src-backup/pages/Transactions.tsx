import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { useStore } from '../store';
import { useDebounced, go } from '../components/hooks';
import { api } from '../mock';
import { Transaction, EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../data';
import { fa, iso, today0, addDays, toLatin } from '../utils';
import {
  Icon,
  Sk,
  RowsSkeleton,
  EmptyState,
  ErrorState,
  Seg,
} from '../components/ui';
import { TxRow } from '../components/TxRow';

const PRESETS: [string, string][] = [
  ['all', 'همه‌ی زمان‌ها'],
  ['today', 'امروز'],
  ['7d', '۷ روز اخیر'],
  ['30d', '۳۰ روز اخیر'],
  ['90d', '۳ ماه اخیر'],
  ['custom', 'بازه‌ی دلخواه'],
];

interface TransactionsProps {
  query: URLSearchParams;
}

interface ListState {
  items: Transaction[];
  cursor: string | null;
  total: number;
  status: 'loading' | 'ready' | 'error';
  more: boolean;
  moreError: boolean;
}

const initialState: ListState = {
  items: [],
  cursor: null,
  total: 0,
  status: 'loading',
  more: false,
  moreError: false,
};

function parseAmount(value: string): number | undefined {
  const normalized = toLatin(value).replace(/[^\d]/g, '');
  if (!normalized) return undefined;

  const amount = Number(normalized);
  return Number.isFinite(amount) && amount >= 0 ? amount : undefined;
}

export function Transactions({ query }: TransactionsProps) {
  const { version, openAdd, openTx } = useStore();

  const [q, setQ] = useState('');
  const [cat, setCat] = useState(query.get('category') || '');
  const [type, setType] = useState('');
  const [preset, setPreset] = useState('all');
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [minAmt, setMinAmt] = useState('');
  const [maxAmt, setMaxAmt] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [st, setSt] = useState<ListState>(initialState);

  const dq = useDebounced(q);
  const busy = useRef(false);
  const requestId = useRef(0);
  const sentinel = useRef<HTMLDivElement>(null);
  const moreRef = useRef<() => void>(() => {});

  const range = useMemo(() => {
    const today = today0();

    if (preset === 'today') {
      return { from: iso(today), to: iso(today) };
    }

    if (preset === '7d') {
      return { from: iso(addDays(today, -6)), to: '' };
    }

    if (preset === '30d') {
      return { from: iso(addDays(today, -29)), to: '' };
    }

    if (preset === '90d') {
      return { from: iso(addDays(today, -89)), to: '' };
    }

    if (preset === 'custom') {
      return { from, to };
    }

    return { from: '', to: '' };
  }, [preset, from, to]);

  const minAmount = useMemo(() => parseAmount(minAmt), [minAmt]);
  const maxAmount = useMemo(() => parseAmount(maxAmt), [maxAmt]);

  const params = useMemo(
    () => ({
      q: dq,
      category: cat,
      type,
      from: range.from,
      to: range.to,
      limit: 15,
      minAmount,
      maxAmount,
    }),
    [dq, cat, type, range.from, range.to, minAmount, maxAmount],
  );

  const first = useCallback(() => {
    const id = ++requestId.current;
    let live = true;

    busy.current = true;
    setSt((previous) => ({
      ...previous,
      status: 'loading',
      more: false,
      moreError: false,
    }));

    api.list(params).then(
      (result) => {
        if (!live || id !== requestId.current) return;

        busy.current = false;
        setSt({
          items: result.items,
          cursor: result.nextCursor,
          total: result.total,
          status: 'ready',
          more: false,
          moreError: false,
        });
      },
      () => {
        if (!live || id !== requestId.current) return;

        busy.current = false;
        setSt({
          items: [],
          cursor: null,
          total: 0,
          status: 'error',
          more: false,
          moreError: false,
        });
      },
    );

    return () => {
      live = false;
    };
  }, [params]);

  useEffect(() => {
    return first();
  }, [first, version]);

  const loadMore = useCallback(() => {
    if (busy.current || !st.cursor || st.status !== 'ready') return;

    const id = requestId.current;
    const cursor = st.cursor;

    busy.current = true;
    setSt((previous) => ({
      ...previous,
      more: true,
      moreError: false,
    }));

    api.list({ ...params, cursor }).then(
      (result) => {
        if (id !== requestId.current) return;

        busy.current = false;
        setSt((previous) => {
          const existingIds = new Set(previous.items.map((item) => item.id));
          const newItems = result.items.filter(
            (item) => !existingIds.has(item.id),
          );

          return {
            ...previous,
            items: [...previous.items, ...newItems],
            cursor: result.nextCursor,
            more: false,
            moreError: false,
          };
        });
      },
      () => {
        if (id !== requestId.current) return;

        busy.current = false;
        setSt((previous) => ({
          ...previous,
          more: false,
          moreError: true,
        }));
      },
    );
  }, [params, st.cursor, st.status]);

  moreRef.current = loadMore;

  useEffect(() => {
    const element = sentinel.current;
    if (!element || st.status !== 'ready' || !st.cursor) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          moreRef.current();
        }
      },
      { rootMargin: '300px' },
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [st.cursor, st.items.length, st.status]);

  const filtered = Boolean(
    dq || cat || type || preset !== 'all' || minAmt || maxAmt,
  );

  const clear = () => {
    setQ('');
    setCat('');
    setType('');
    setPreset('all');
    setFrom('');
    setTo('');
    setMinAmt('');
    setMaxAmt('');
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
    boxSizing: 'border-box',
  };

  const selectStyle: React.CSSProperties = {
    ...inputStyle,
    width: 'auto',
    minWidth: 140,
    appearance: 'none',
    WebkitAppearance: 'none',
    paddingInlineEnd: 34,
    backgroundImage:
      'url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2712%27 height=%278%27 fill=%27none%27 stroke=%27%238f97a8%27 stroke-width=%271.6%27%3E%3Cpath d=%27M1 1.5l5 5 5-5%27/%3E%3C/svg%3E")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'left 12px center',
  };

  const exportCSV = () => {
    const rows: string[][] = [
      ['تاریخ', 'نام', 'دسته', 'نوع', 'مبلغ', 'وضعیت'],
    ];

    st.items.forEach((transaction) => {
      rows.push([
        transaction.date,
        transaction.name,
        transaction.category,
        transaction.type === 'income' ? 'درآمد' : 'هزینه',
        String(transaction.amount),
        transaction.status === 'completed' ? 'انجام‌شده' : 'در انتظار',
      ]);
    });

    const escapeCSV = (value: string) =>
      `"${value.replace(/"/g, '""')}"`;

    const csv = rows.map((row) => row.map(escapeCSV).join(',')).join('\r\n');
    const blob = new Blob(['\uFEFF', csv], {
      type: 'text/csv;charset=utf-8;',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.href = url;
    link.download = 'payo-transactions.csv';
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  };

  const dateRangeInvalid = Boolean(
    preset === 'custom' && from && to && from > to,
  );

  const amountRangeInvalid = Boolean(
    minAmount !== undefined &&
      maxAmount !== undefined &&
      minAmount > maxAmount,
  );

  return (
    <div
      style={{
        maxWidth: 1180,
        margin: '0 auto',
        padding: '28px 20px 80px',
        animation: 'pagein 0.25s ease both',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
          marginBottom: 20,
          flexWrap: 'wrap',
        }}
      >
        <h1
          style={{
            fontSize: 22,
            fontWeight: 600,
            letterSpacing: '-0.01em',
            margin: 0,
          }}
        >
          تراکنش‌ها
        </h1>

        <div style={{ display: 'flex', gap: 8 }}>
          <button
            onClick={exportCSV}
            disabled={st.items.length === 0}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              height: 38,
              padding: '0 14px',
              borderRadius: 'var(--radius)',
              fontSize: 13,
              border: '1px solid var(--border-strong)',
              background: 'rgba(255,255,255,.02)',
              color: 'var(--text-secondary)',
              cursor: st.items.length ? 'pointer' : 'not-allowed',
              opacity: st.items.length ? 1 : 0.5,
              fontFamily: 'inherit',
            }}
          >
            <Icon n="download" s={16} />
            CSV
          </button>

          <button
            onClick={() => openAdd('expense')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              height: 38,
              padding: '0 16px',
              borderRadius: 'var(--radius)',
              fontSize: 13,
              fontWeight: 500,
              background: 'var(--accent-blue)',
              color: '#fff',
              border: 'none',
              cursor: 'pointer',
              fontFamily: 'inherit',
            }}
          >
            <Icon n="plus" s={16} />
            ثبت
          </button>
        </div>
      </div>

      {/* Filters */}
      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
          padding: 16,
          marginBottom: 16,
        }}
      >
        <div
          style={{
            display: 'flex',
            gap: 10,
            flexWrap: 'wrap',
            alignItems: 'center',
          }}
        >
          <div style={{ position: 'relative', flex: '1 1 220px' }}>
            <span
              style={{
                position: 'absolute',
                insetInlineStart: 13,
                top: 12,
                color: 'var(--text-tertiary)',
              }}
            >
              <Icon n="search" s={18} />
            </span>

            <input
              className="input"
              style={{ ...inputStyle, paddingInlineStart: 40 }}
              placeholder="جست‌وجوی نام یا دسته"
              value={q}
              onChange={(event) => setQ(event.target.value)}
              aria-label="جست‌وجو"
            />
          </div>

          <select
            style={selectStyle}
            value={cat}
            onChange={(event) => setCat(event.target.value)}
            aria-label="دسته"
          >
            <option value="">همه‌ی دسته‌ها</option>
            <optgroup label="هزینه">
              {EXPENSE_CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </optgroup>
            <optgroup label="درآمد">
              {INCOME_CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </optgroup>
          </select>

          <select
            style={selectStyle}
            value={preset}
            onChange={(event) => setPreset(event.target.value)}
            aria-label="بازه‌ی زمانی"
          >
            {PRESETS.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>

          <Seg
            options={[
              ['', 'همه'],
              ['income', 'درآمد'],
              ['expense', 'هزینه'],
            ]}
            value={type}
            onChange={setType}
          />

          <button
            onClick={() => setShowAdvanced((value) => !value)}
            aria-expanded={showAdvanced}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              height: 38,
              padding: '0 12px',
              borderRadius: 'var(--radius)',
              fontSize: 13,
              border: '1px solid var(--border)',
              background: showAdvanced ? 'var(--accent-soft)' : 'none',
              color: showAdvanced
                ? 'var(--accent-blue)'
                : 'var(--text-secondary)',
              cursor: 'pointer',
              fontFamily: 'inherit',
            }}
          >
            <Icon n="filter" s={16} />
            فیلتر پیشرفته
          </button>
        </div>

        {preset === 'custom' && (
          <div
            style={{
              display: 'flex',
              gap: 10,
              marginTop: 10,
              flexWrap: 'wrap',
            }}
          >
            <input
              type="date"
              style={{ ...inputStyle, width: 'auto' }}
              value={from}
              max={iso(today0())}
              onChange={(event) => setFrom(event.target.value)}
              aria-label="از تاریخ"
            />

            <input
              type="date"
              style={{ ...inputStyle, width: 'auto' }}
              value={to}
              min={from || undefined}
              max={iso(today0())}
              onChange={(event) => setTo(event.target.value)}
              aria-label="تا تاریخ"
            />
          </div>
        )}

        {dateRangeInvalid && (
          <p style={{ color: 'var(--danger)', fontSize: 12, marginBottom: 0 }}>
            تاریخ شروع نباید بعد از تاریخ پایان باشد.
          </p>
        )}

        {showAdvanced && (
          <div
            style={{
              display: 'flex',
              gap: 10,
              marginTop: 10,
              flexWrap: 'wrap',
            }}
          >
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 5,
                flex: '1 1 180px',
              }}
            >
              <label
                style={{ fontSize: 12, color: 'var(--text-secondary)' }}
              >
                حداقل مبلغ (تومان)
              </label>
              <input
                inputMode="numeric"
                style={inputStyle}
                placeholder="مثلاً ۱۰۰۰۰۰"
                value={minAmt}
                onChange={(event) => setMinAmt(event.target.value)}
              />
            </div>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 5,
                flex: '1 1 180px',
              }}
            >
              <label
                style={{ fontSize: 12, color: 'var(--text-secondary)' }}
              >
                حداکثر مبلغ (تومان)
              </label>
              <input
                inputMode="numeric"
                style={inputStyle}
                placeholder="مثلاً ۵۰۰۰۰۰۰"
                value={maxAmt}
                onChange={(event) => setMaxAmt(event.target.value)}
              />
            </div>
          </div>
        )}

        {amountRangeInvalid && (
          <p style={{ color: 'var(--danger)', fontSize: 12, marginBottom: 0 }}>
            حداقل مبلغ نباید از حداکثر مبلغ بیشتر باشد.
          </p>
        )}
      </div>

      {/* Meta */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
          color: 'var(--text-secondary)',
          fontSize: 13,
          marginBottom: 10,
        }}
      >
        <span>
          {st.status === 'ready' ? `${fa(st.total)} تراکنش` : ''}
        </span>

        {filtered && (
          <button
            onClick={clear}
            style={{
              height: 30,
              padding: '0 10px',
              borderRadius: 'var(--radius)',
              fontSize: 13,
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              background: 'none',
              border: 'none',
              fontFamily: 'inherit',
            }}
          >
            پاک‌کردن فیلترها
          </button>
        )}
      </div>

      {/* Transaction list */}
      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
          padding: 8,
          minWidth: 0,
        }}
      >
        {dateRangeInvalid || amountRangeInvalid ? (
          <EmptyState
            title="فیلترها معتبر نیستند."
            text="بازه‌ی تاریخ یا مبلغ را اصلاح کن."
          />
        ) : st.status === 'loading' ? (
          <RowsSkeleton n={8} />
        ) : st.status === 'error' ? (
          <ErrorState
            title="مشکلی پیش آمد."
            text="تراکنش‌هایت بارگذاری نشد."
            onRetry={first}
          />
        ) : st.items.length === 0 ? (
          filtered ? (
            <EmptyState
              title="چیزی پیدا نشد."
              text="فیلترها را تغییر بده یا همه را پاک کن."
            />
          ) : (
            <EmptyState
              title="هنوز تراکنشی نیست."
              text="اولین درآمد یا هزینه‌ات را ثبت کن."
              cta="ثبت تراکنش"
              onCta={() => openAdd('expense')}
            />
          )
        ) : (
          <>
            {st.items.map((transaction, index) => (
              <TxRow
                key={transaction.id}
                t={transaction}
                i={index < 15 ? index : 0}
                full
                onClick={() => openTx(transaction)}
              />
            ))}

            {st.more && <RowsSkeleton n={2} />}

            {st.moreError && (
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 10,
                  padding: 16,
                  color: 'var(--text-secondary)',
                  fontSize: 13,
                }}
              >
                <span>بارگذاری تراکنش‌های بعدی ناموفق بود.</span>
                <button
                  onClick={loadMore}
                  style={{
                    color: 'var(--accent-blue)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    font: 'inherit',
                  }}
                >
                  تلاش دوباره
                </button>
              </div>
            )}

            {st.cursor && !st.more && !st.moreError && (
              <button
                onClick={loadMore}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: 12,
                  color: 'var(--accent-blue)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  font: 'inherit',
                  fontSize: 13,
                }}
              >
                نمایش تراکنش‌های بیشتر
              </button>
            )}

            <div ref={sentinel} style={{ height: 1 }} />
          </>
        )}
      </div>
    </div>
  );
}
