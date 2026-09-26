import React from 'react';
import { useApi, useCountUp, go } from '../components/hooks';
import { api } from '../mock';
import { useStore } from '../store';
import { fa, short, pctText } from '../utils';
import {
  Icon,
  Sk,
  RowsSkeleton,
  EmptyState,
  ErrorState,
  AlertBanner,
  ProgressBar,
} from '../components/ui';
import { TxRow } from '../components/TxRow';
import { Sparkline } from '../components/Sparkline';
import { getCategoryColor } from '../data';

function clampPct(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(100, value));
}

function StatCard({
  title,
  value,
  note,
  pct,
  hatch,
}: {
  title: string;
  value: number;
  note: string;
  pct: number;
  hatch?: boolean;
}) {
  const v = useCountUp(Number.isFinite(value) ? value : 0);

  return (
    <div
      style={{
        background:
          'linear-gradient(180deg,rgba(255,255,255,.03),rgba(255,255,255,.008)),var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-lg)',
        padding: 20,
        position: 'relative',
        transition: 'transform 0.25s, border-color 0.25s',
        minWidth: 0,
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-2px)';
        e.currentTarget.style.borderColor = 'var(--border-strong)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = '';
        e.currentTarget.style.borderColor = '';
      }}
    >
      <div
        style={{
          fontSize: 13,
          color: 'var(--text-secondary)',
          fontWeight: 500,
          marginBottom: 6,
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontSize: 22,
          fontWeight: 500,
          letterSpacing: '-0.01em',
          fontFamily: 'var(--font-mono, monospace)',
          marginTop: 4,
          overflowWrap: 'anywhere',
        }}
      >
        {fa(v)}{' '}
        <span
          style={{
            fontSize: 13,
            color: 'var(--text-secondary)',
            fontWeight: 400,
          }}
        >
          تومان
        </span>
      </div>

      <div
        style={{
          fontSize: 12,
          color: 'var(--text-secondary)',
          marginTop: 4,
        }}
      >
        {note}
      </div>

      <div style={{ marginTop: 12 }}>
        <ProgressBar
          pct={clampPct(pct)}
          color={hatch ? 'var(--text-tertiary)' : undefined}
        />
      </div>
    </div>
  );
}

function Panel({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <section
      style={{
        background:
          'linear-gradient(180deg,rgba(255,255,255,.03),rgba(255,255,255,.008)),var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-lg)',
        minWidth: 0,
        ...style,
      }}
    >
      {children}
    </section>
  );
}

export function Dashboard() {
  const { version, openAdd, openTx, budgetAlerts } = useStore();

  const sum = useApi(() => api.summary(), [version]);
  const rec = useApi(() => api.list({ limit: 6 }), [version]);
  const cats = useApi(() => api.categories('30d'), [version]);
  const ins = useApi(() => api.insights('30d'), [version]);
  const budgetSt = useApi(() => api.budgetStatus(), [version]);

  const balance = useCountUp(sum.data?.balance || 0, 1200);
  const s = sum.data;

  const retryAll = () => {
    sum.reload();
    rec.reload();
    cats.reload();
    ins.reload();
    budgetSt.reload();
  };

  const insightColor = {
    info: 'var(--accent-blue)',
    warning: 'var(--warning)',
    success: 'var(--success)',
  };

  if (sum.status === 'error') {
    return (
      <div className="page">
        <div className="card">
          <ErrorState
            title="مشکلی پیش آمد."
            text="اطلاعات مالی‌ات بارگذاری نشد."
            onRetry={retryAll}
          />
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: 1180,
        margin: '0 auto',
        padding: '28px 20px 80px',
        animation: 'pagein 0.25s ease both',
      }}
    >
      {budgetAlerts.length > 0 && <AlertBanner alerts={budgetAlerts} />}

      <div
        className="dashboard-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(12, minmax(0, 1fr))',
          gap: 16,
          alignItems: 'start',
        }}
      >
        {/* Balance */}
        <Panel
          style={{
            gridColumn: '1 / 9',
            padding: 24,
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 12,
              flexWrap: 'wrap',
            }}
          >
            <span
              style={{
                fontSize: 13,
                color: 'var(--text-secondary)',
                fontWeight: 500,
              }}
            >
              موجودی فعلی
            </span>

            {s && (
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  minHeight: 24,
                  padding: '0 9px',
                  borderRadius: 5,
                  fontSize: 12,
                  fontWeight: 500,
                  border: '1px solid rgba(61,220,151,.35)',
                  color: 'var(--success)',
                  background: 'rgba(61,220,151,.07)',
                }}
              >
                <Icon n="up" s={13} />
                {s.changePct.toLocaleString('fa-IR')}٪ نسبت به ماه قبل
              </span>
            )}
          </div>

          {!s ? (
            <>
              <Sk w="60%" h={48} style={{ margin: '14px 0' }} />
              <Sk h={84} />
            </>
          ) : (
            <>
              <div
                style={{
                  fontSize: 'clamp(32px, 5vw, 52px)',
                  fontWeight: 500,
                  letterSpacing: '-0.02em',
                  lineHeight: 1.15,
                  margin: '10px 0 4px',
                  fontFamily: 'var(--font-mono, monospace)',
                  overflowWrap: 'anywhere',
                }}
              >
                {fa(balance)}
                <small
                  style={{
                    fontSize: '0.32em',
                    color: 'var(--text-secondary)',
                    fontWeight: 400,
                    marginInlineStart: 8,
                  }}
                >
                  تومان
                </small>
              </div>

              <Sparkline data={s.trend} />
            </>
          )}

          <div
            style={{
              display: 'flex',
              gap: 10,
              marginTop: 18,
              flexWrap: 'wrap',
            }}
          >
            <button
              onClick={() => openAdd('expense')}
              style={{
                flex: '1 1 140px',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 8,
                minHeight: 42,
                borderRadius: 'var(--radius)',
                fontWeight: 500,
                fontSize: 14,
                background: 'var(--accent-blue)',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
                transition: 'transform 0.15s, background 0.15s',
                boxShadow:
                  '0 0 0 1px rgba(255,255,255,.14) inset, 0 10px 30px -10px var(--accent-glow)',
                fontFamily: 'inherit',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = '';
              }}
            >
              <Icon n="down" s={18} />
              ثبت هزینه
            </button>

            <button
              onClick={() => openAdd('income')}
              style={{
                flex: '1 1 140px',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 8,
                minHeight: 42,
                borderRadius: 'var(--radius)',
                fontWeight: 500,
                fontSize: 14,
                border: '1px solid var(--border-strong)',
                background: 'rgba(255,255,255,.02)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                transition: 'transform 0.15s, background 0.15s',
                fontFamily: 'inherit',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,.07)';
                e.currentTarget.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,.02)';
                e.currentTarget.style.transform = '';
              }}
            >
              <Icon n="up" s={18} />
              ثبت درآمد
            </button>
          </div>
        </Panel>

        {/* Stats */}
        <div
          style={{
            gridColumn: '9 / 13',
            gridRow: '1 / 3',
            display: 'flex',
            flexDirection: 'column',
            gap: 12,
            minWidth: 0,
          }}
        >
          {!s ? (
            <>
              <Sk h={100} style={{ borderRadius: 12 }} />
              <Sk h={100} style={{ borderRadius: 12 }} />
              <Sk h={100} style={{ borderRadius: 12 }} />
            </>
          ) : (
            <>
              <StatCard
                title="درآمد ۳۰ روز"
                value={s.income}
                note={pctText(s.income, s.prevIncome)}
                pct={
                  (s.income /
                    Math.max(s.income, s.prevIncome, 1)) *
                  100
                }
              />

              <StatCard
                title="هزینه‌ها ۳۰ روز"
                value={s.expenses}
                note={pctText(s.expenses, s.prevExpenses)}
                pct={
                  (s.expenses /
                    Math.max(s.expenses, s.prevExpenses, 1)) *
                  100
                }
                hatch
              />

              <StatCard
                title="پس‌انداز ۳۰ روز"
                value={s.savings}
                note={
                  fa(
                    s.income
                      ? Math.round((s.savings / s.income) * 100)
                      : 0,
                  ) + '٪ از درآمد'
                }
                pct={
                  s.income
                    ? (s.savings / s.income) * 100
                    : 0
                }
              />
            </>
          )}
        </div>

        {/* Recent transactions */}
        <Panel
          style={{
            gridColumn: '1 / 9',
            padding: '20px 8px',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 12,
              marginBottom: 6,
              padding: '0 6px',
            }}
          >
            <span
              style={{
                fontSize: 13,
                color: 'var(--text-secondary)',
                fontWeight: 500,
              }}
            >
              آخرین تراکنش‌ها
            </span>

            <a
              href="#/tx"
              style={{
                minHeight: 30,
                padding: '0 10px',
                borderRadius: 'var(--radius)',
                fontSize: 13,
                color: 'var(--text-secondary)',
                display: 'inline-flex',
                alignItems: 'center',
                cursor: 'pointer',
                transition: 'color 0.15s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = 'var(--text-secondary)';
              }}
            >
              همه
            </a>
          </div>

          {rec.status === 'error' ? (
            <ErrorState
              title="تراکنش‌ها بارگذاری نشدند."
              text="لطفاً دوباره تلاش کن."
              onRetry={rec.reload}
            />
          ) : !rec.data ? (
            <RowsSkeleton n={6} />
          ) : rec.data.items.length === 0 ? (
            <EmptyState
              title="هنوز تراکنشی نیست."
              text="اولین درآمد یا هزینه‌ات را ثبت کن."
              cta="ثبت تراکنش"
              onCta={() => openAdd('expense')}
            />
          ) : (
            rec.data.items.map((t, i) => (
              <TxRow
                key={t.id}
                t={t}
                i={i}
                onClick={() => openTx(t)}
              />
            ))
          )}
        </Panel>

        {/* Categories */}
        <Panel
          style={{
            gridColumn: '9 / 13',
            padding: 20,
          }}
        >
          <div
            style={{
              fontSize: 13,
              color: 'var(--text-secondary)',
              fontWeight: 500,
              marginBottom: 14,
            }}
          >
            هزینه‌ها · ۳۰ روز
          </div>

          {cats.status === 'error' ? (
            <ErrorState
              title="دسته‌بندی‌ها بارگذاری نشدند."
              text="لطفاً دوباره تلاش کن."
              onRetry={cats.reload}
            />
          ) : !cats.data ? (
            <Sk h={120} />
          ) : cats.data.length === 0 ? (
            <p
              style={{
                color: 'var(--text-secondary)',
                fontSize: 13,
              }}
            >
              هنوز هزینه‌ای ثبت نشده.
            </p>
          ) : (
            <div>
              <div
                style={{
                  display: 'flex',
                  height: 10,
                  borderRadius: 3,
                  overflow: 'hidden',
                  gap: 2,
                  marginBottom: 14,
                }}
              >
                {cats.data.slice(0, 5).map((c, i) => (
                  <div
                    key={c.category}
                    title={c.category}
                    style={{
                      flex: Math.max(0, c.share),
                      background: getCategoryColor(c.category),
                      animation: `grow 0.8s cubic-bezier(0.2,0.7,0.2,1) ${i * 60}ms both`,
                    }}
                  />
                ))}
              </div>

              {cats.data.slice(0, 5).map((c) => (
                <button
                  key={c.category}
                  onClick={() =>
                    go(
                      '/tx?category=' +
                        encodeURIComponent(c.category),
                    )
                  }
                  style={{
                    display: 'grid',
                    gridTemplateColumns:
                      'minmax(70px, 90px) minmax(30px, 1fr) auto',
                    gap: 10,
                    alignItems: 'center',
                    padding: '8px 6px',
                    borderRadius: 6,
                    cursor: 'pointer',
                    transition: 'background 0.15s',
                    width: '100%',
                    textAlign: 'start',
                    background: 'none',
                    border: 'none',
                    color: 'inherit',
                    fontFamily: 'inherit',
                    minWidth: 0,
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background =
                      'rgba(255,255,255,0.04)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'none';
                  }}
                >
                  <span
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 7,
                      fontSize: 13,
                      minWidth: 0,
                      overflowWrap: 'anywhere',
                    }}
                  >
                    <i
                      style={{
                        width: 7,
                        height: 7,
                        borderRadius: 2,
                        background: getCategoryColor(c.category),
                        flexShrink: 0,
                      }}
                    />
                    {c.category}
                  </span>

                  <div
                    style={{
                      height: 5,
                      background: 'rgba(255,255,255,0.06)',
                      borderRadius: 2,
                      overflow: 'hidden',
                    }}
                  >
                    <div
                      style={{
                        width: `${clampPct(c.share)}%`,
                        height: '100%',
                        background: getCategoryColor(c.category),
                        transformOrigin: 'right',
                        animation:
                          'grow 0.8s cubic-bezier(0.2,0.7,0.2,1) both',
                      }}
                    />
                  </div>

                  <span
                    style={{
                      fontSize: 12,
                      color: 'var(--text-secondary)',
                      fontFamily: 'var(--font-mono, monospace)',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {short(c.amount)}
                  </span>
                </button>
              ))}
            </div>
          )}
        </Panel>

        {/* Budget quick view */}
        {budgetSt.data && budgetSt.data.length > 0 && (
          <Panel
            style={{
              gridColumn: '1 / 7',
              padding: 20,
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: 12,
                marginBottom: 14,
              }}
            >
              <span
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  fontWeight: 500,
                }}
              >
                بودجه‌ی این ماه
              </span>

              <a
                href="#/budget"
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  cursor: 'pointer',
                }}
              >
                مدیریت
              </a>
            </div>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 10,
              }}
            >
              {budgetSt.data.slice(0, 4).map((b) => (
                <div key={b.category}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      gap: 10,
                      marginBottom: 5,
                      fontSize: 13,
                    }}
                  >
                    <span
                      style={{
                        color: 'var(--text-secondary)',
                        overflowWrap: 'anywhere',
                      }}
                    >
                      {b.category}
                    </span>

                    <span
                      style={{
                        color:
                          b.pct >= 100
                            ? 'var(--danger)'
                            : b.pct >= 80
                              ? 'var(--warning)'
                              : 'var(--text-secondary)',
                        fontFamily: 'var(--font-mono, monospace)',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {fa(b.pct)}٪
                    </span>
                  </div>

                  <ProgressBar pct={clampPct(b.pct)} />
                </div>
              ))}
            </div>
          </Panel>
        )}

        {/* Insights */}
        <Panel
          style={{
            gridColumn: budgetSt.data?.length ? '7 / 13' : '1 / 13',
            padding: 20,
          }}
        >
          <div
            style={{
              fontSize: 13,
              color: 'var(--text-secondary)',
              fontWeight: 500,
              marginBottom: 4,
            }}
          >
            این ماه چه تغییری کرد؟
          </div>

          {ins.status === 'error' ? (
            <ErrorState
              title="تحلیل‌ها بارگذاری نشدند."
              text="لطفاً دوباره تلاش کن."
              onRetry={ins.reload}
            />
          ) : !ins.data ? (
            <Sk h={90} style={{ marginTop: 12 }} />
          ) : ins.data.length === 0 ? (
            <p
              style={{
                color: 'var(--text-secondary)',
                fontSize: 13,
                marginTop: 12,
              }}
            >
              هنوز تحلیلی برای نمایش وجود ندارد.
            </p>
          ) : (
            ins.data.slice(0, 3).map((x, i) => (
              <div
                key={x.id}
                style={{
                  display: 'flex',
                  gap: 12,
                  padding: '12px 0',
                  borderBottom:
                    i === Math.min(ins.data!.length, 3) - 1
                      ? 'none'
                      : '1px solid var(--border)',
                  fontSize: 14,
                }}
              >
                <span
                  style={{
                    color:
                      insightColor[
                        (x.type || 'info') as keyof typeof insightColor
                      ] || 'var(--accent-blue)',
                    flexShrink: 0,
                    marginTop: 4,
                  }}
                >
                  <Icon
                    n={
                      x.type === 'warning'
                        ? 'warning'
                        : x.type === 'success'
                          ? 'check'
                          : 'trend'
                    }
                    s={17}
                  />
                </span>

                <span
                  style={{
                    color: 'var(--text-secondary)',
                    overflowWrap: 'anywhere',
                  }}
                >
                  {x.text}
                </span>
              </div>
            ))
          )}
        </Panel>
      </div>

      {/* Security */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          gap: 20,
          flexWrap: 'wrap',
          color: 'var(--text-tertiary)',
          fontSize: 12.5,
          marginTop: 40,
        }}
      >
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
          }}
        >
          <Icon n="lock" s={14} />
          اتصال امن
        </span>

        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
          }}
        >
          <Icon n="shield" s={14} />
          حساب محافظت‌شده
        </span>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .dashboard-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
          }
          .dashboard-grid > * {
            grid-column: 1 / -1 !important;
            grid-row: auto !important;
          }
        }
      `}</style>
    </div>
  );
}
