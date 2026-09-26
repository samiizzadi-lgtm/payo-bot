import React from 'react';
import { Transaction, getCategoryColor } from '../data';
import { fa, toman, dateLabel } from '../utils';
import { Icon } from './ui';

interface TxRowProps {
  t: Transaction;
  i?: number;
  full?: boolean;
  onClick: () => void;
}

export function TxRow({
  t,
  i = 0,
  full = false,
  onClick,
}: TxRowProps) {
  const inc = t.type === 'income';
  const color = getCategoryColor(t.category);

  const columns = full
    ? '40px minmax(0, 1.6fr) 120px 110px auto'
    : '40px minmax(0, 1fr) auto';

  const handleMouseEnter = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.currentTarget.style.background =
      'rgba(255,255,255,0.035)';
  };

  const handleMouseLeave = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.currentTarget.style.background = 'none';
  };

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={
        (inc ? 'درآمد ' : 'هزینه ') +
        t.name +
        '، ' +
        toman(t.amount)
      }
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        display: 'grid',
        gridTemplateColumns: columns,
        gap: 12,
        alignItems: 'center',
        padding: full ? '14px 12px' : '13px 6px',
        borderBottom: '1px solid var(--border)',
        cursor: 'pointer',
        transition: 'background 0.15s',
        borderRadius: 6,
        animation:
          'rowin 0.35s cubic-bezier(0.2,0.7,0.2,1) both',
        animationDelay: `${i * 22}ms`,
        width: '100%',
        textAlign: 'start',
        background: 'none',
        border: 'none',
        color: 'inherit',
        fontFamily: 'inherit',
      }}
    >
      {/* Icon */}
      <span
        style={{
          width: 36,
          height: 36,
          borderRadius: 8,
          display: 'grid',
          placeItems: 'center',
          border: inc
            ? '1px solid rgba(61,220,151,0.4)'
            : '1px solid var(--border-strong)',
          background: inc
            ? 'rgba(61,220,151,0.07)'
            : 'rgba(255,255,255,0.02)',
          color: inc
            ? 'var(--success)'
            : 'var(--text-secondary)',
          flexShrink: 0,
        }}
      >
        <Icon n={inc ? 'up' : 'down'} s={16} />
      </span>

      {/* Name + meta */}
      <span style={{ minWidth: 0 }}>
        <span
          style={{
            display: 'block',
            fontWeight: 500,
            fontSize: 14.5,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}
        >
          {t.name}
        </span>

        <span
          style={{
            fontSize: 12.5,
            color: 'var(--text-secondary)',
            display: 'flex',
            gap: 8,
            alignItems: 'center',
            flexWrap: 'wrap',
            marginTop: 2,
          }}
        >
          <span
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 5,
            }}
          >
            <i
              aria-hidden="true"
              style={{
                width: 7,
                height: 7,
                borderRadius: 2,
                display: 'inline-block',
                background: color,
                flexShrink: 0,
              }}
            />
            {t.category}
          </span>

          {!full && <span>{dateLabel(t.date)}</span>}

          {!full && t.status === 'pending' && (
            <span
              style={{
                color: 'var(--warning)',
                fontSize: 12,
              }}
            >
              در انتظار
            </span>
          )}
        </span>
      </span>

      {/* Date column */}
      {full && (
        <span
          style={{
            fontSize: 13,
            color: 'var(--text-secondary)',
          }}
        >
          {dateLabel(t.date)}
        </span>
      )}

      {/* Status column */}
      {full && (
        <span
          style={{
            fontSize: 13,
            color: 'var(--text-secondary)',
          }}
        >
          {t.status === 'pending' ? (
            <span style={{ color: 'var(--warning)' }}>
              در انتظار
            </span>
          ) : (
            'انجام‌شده'
          )}
        </span>
      )}

      {/* Amount */}
      <span
        style={{
          fontWeight: 500,
          fontSize: 15,
          textAlign: 'end',
          direction: 'ltr',
          whiteSpace: 'nowrap',
          color: inc
            ? 'var(--success)'
            : 'var(--text-primary)',
          fontFamily: 'var(--font-mono, monospace)',
        }}
      >
        {inc ? '+' : '−'}
        {fa(t.amount)}

        <small
          style={{
            display: 'block',
            fontSize: 11.5,
            color: 'var(--text-secondary)',
            fontWeight: 400,
            direction: 'rtl',
            fontFamily: 'inherit',
          }}
        >
          تومان
        </small>
      </span>
    </button>
  );
}
