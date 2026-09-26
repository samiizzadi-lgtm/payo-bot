import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
} from 'react';

/* ── Icons ── */
export const ICONS: Record<string, string> = {
  home: 'M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z',
  list: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01',
  chart: 'M4 20V10M10 20V4M16 20v-7M22 20H2',
  wallet: 'M2 8h20v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8zM2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v2M12 14h.01',
  plus: 'M12 5v14M5 12h14',
  search: 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-4.5-4.5',
  up: 'M12 19V5M6 11l6-6 6 6',
  down: 'M12 5v14M6 13l6 6 6-6',
  check: 'M5 12.5l4.5 4.5L19 7',
  x: 'M6 6l12 12M18 6L6 18',
  lock: 'M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3',
  shield: 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z',
  more: 'M5 12h.01M12 12h.01M19 12h.01',
  trash: 'M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13',
  trend: 'M3 17l6-6 4 4 8-9M15 6h6v6',
  back: 'M9 6l6 6-6 6',
  bell: 'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0',
  target: 'M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM12 7a5 5 0 1 0 0 10A5 5 0 0 0 12 7zM12 12h.01',
  edit: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z',
  download: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3',
  filter: 'M4 6h16M8 12h8M11 18h2',
  star: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
  info: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 8v4M12 16h.01',
  warning: 'M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01',
  print: 'M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v8H6z',
};

export function Icon({
  n,
  s = 20,
}: {
  n: string;
  s?: number;
}) {
  return (
    <svg
      width={s}
      height={s}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.7}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d={ICONS[n] || ''} />
    </svg>
  );
}

/* ── Logo ── */
export function Logo({ size }: { size?: number }) {
  const logoSize = size ?? 24;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 9,
        fontWeight: 600,
        fontSize: 18,
        letterSpacing: '-0.02em',
        direction: 'ltr',
      }}
      aria-label="Payo"
    >
      <svg
        viewBox="0 0 32 32"
        style={{
          width: logoSize,
          height: logoSize,
          flexShrink: 0,
        }}
        aria-hidden="true"
      >
        <path
          fillRule="evenodd"
          fill="currentColor"
          d="M6 4h10a9 9 0 0 1 0 18h-4v6H6zM12 10h4a3 3 0 0 1 0 6h-4z"
        />
        <rect
          x="6"
          y="24"
          width="6"
          height="4"
          fill="#2f6bff"
        />
      </svg>
      <span>Payo</span>
    </span>
  );
}

/* ── Skeleton ── */
export function Sk({
  w = '100%',
  h = 16,
  style,
}: {
  w?: string | number;
  h?: number;
  style?: React.CSSProperties;
}) {
  return (
    <div
      aria-hidden="true"
      style={{
        width: w,
        height: h,
        background:
          'linear-gradient(90deg,rgba(255,255,255,.04),rgba(255,255,255,.1),rgba(255,255,255,.04))',
        backgroundSize: '200% 100%',
        animation: 'sk 1.4s linear infinite',
        borderRadius: 5,
        ...style,
      }}
    />
  );
}

export function RowsSkeleton({ n = 5 }: { n?: number }) {
  const count = Math.max(0, Math.floor(n));

  return (
    <div aria-hidden="true">
      {Array.from({ length: count }, (_, i) => (
        <div
          key={i}
          style={{
            display: 'grid',
            gridTemplateColumns: '40px 1fr auto',
            gap: 12,
            alignItems: 'center',
            padding: '13px 6px',
            borderBottom: '1px solid var(--border)',
          }}
        >
          <Sk w="36px" h={36} />
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 8,
            }}
          >
            <Sk w="55%" h={13} />
            <Sk w="35%" h={11} />
          </div>
          <Sk w="80px" h={13} />
        </div>
      ))}
    </div>
  );
}

/* ── Empty State ── */
export function EmptyState({
  title,
  text,
  cta,
  onCta,
}: {
  title: string;
  text: string;
  cta?: string | null;
  onCta?: () => void;
}) {
  return (
    <div
      style={{
        textAlign: 'center',
        padding: '56px 20px',
      }}
    >
      <div
        style={{
          width: 48,
          height: 48,
          margin: '0 auto 18px',
          border: '1px solid var(--border-strong)',
          borderRadius: 8,
          display: 'grid',
          placeItems: 'center',
          color: 'var(--accent-blue)',
        }}
      >
        <Icon n="trend" />
      </div>

      <h3
        style={{
          fontSize: 18,
          fontWeight: 600,
          marginBottom: 6,
        }}
      >
        {title}
      </h3>

      <p
        style={{
          color: 'var(--text-secondary)',
          maxWidth: 340,
          margin: '0 auto 20px',
        }}
      >
        {text}
      </p>

      {cta && (
        <button
          type="button"
          onClick={onCta}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            height: 42,
            padding: '0 18px',
            borderRadius: 'var(--radius)',
            fontWeight: 500,
            fontSize: 14,
            background: 'var(--accent-blue)',
            color: '#fff',
            border: 'none',
            cursor: onCta ? 'pointer' : 'default',
          }}
        >
          <Icon n="plus" s={18} />
          {cta}
        </button>
      )}
    </div>
  );
}

/* ── Error State ── */
export function ErrorState({
  title,
  text,
  onRetry,
}: {
  title: string;
  text: string;
  onRetry: () => void;
}) {
  return (
    <div
      style={{
        textAlign: 'center',
        padding: '56px 20px',
      }}
    >
      <div
        style={{
          width: 48,
          height: 48,
          margin: '0 auto 18px',
          border: '1px solid rgba(255,93,108,.3)',
          borderRadius: 8,
          display: 'grid',
          placeItems: 'center',
          color: 'var(--danger)',
        }}
      >
        <Icon n="x" />
      </div>

      <h3
        style={{
          fontSize: 18,
          fontWeight: 600,
          marginBottom: 6,
        }}
      >
        {title}
      </h3>

      <p
        style={{
          color: 'var(--text-secondary)',
          maxWidth: 340,
          margin: '0 auto 20px',
        }}
      >
        {text}
      </p>

      <button
        type="button"
        onClick={onRetry}
        style={{
          height: 42,
          padding: '0 18px',
          borderRadius: 'var(--radius)',
          fontWeight: 500,
          fontSize: 14,
          border: '1px solid var(--border-strong)',
          background: 'rgba(255,255,255,.02)',
          color: 'var(--text-primary)',
          cursor: 'pointer',
        }}
      >
        تلاش دوباره
      </button>
    </div>
  );
}

/* ── Modal ── */
type ModalProps = {
  title: string;
  onClose: () => void;
  children:
    | React.ReactNode
    | ((close: () => void) => React.ReactNode);
};

export function Modal({
  title,
  onClose,
  children,
}: ModalProps) {
  const [out, setOut] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const closingRef = useRef(false);
  const onCloseRef = useRef(onClose);

  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);

  const close = useCallback(() => {
    if (closingRef.current) return;

    closingRef.current = true;
    setOut(true);

    window.setTimeout(() => {
      onCloseRef.current();
    }, 160);
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.stopPropagation();
        close();
      }
    };

    const previousOverflow = document.body.style.overflow;

    window.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';

    const firstFocusable =
      ref.current?.querySelector<HTMLElement>(
        'input:not([disabled]), button:not([disabled]), select:not([disabled]), textarea:not([disabled])'
      );

    firstFocusable?.focus({ preventScroll: true });

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [close]);

  const isMobile =
    typeof window !== 'undefined' &&
    window.innerWidth < 760;

  const handleBackdropMouseDown = (
    event: React.MouseEvent<HTMLDivElement>
  ) => {
    if (event.target === event.currentTarget) {
      close();
    }
  };

  return (
    <div
      onMouseDown={handleBackdropMouseDown}
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 100,
        background: 'rgba(0,0,0,0.72)',
        backdropFilter: 'blur(6px)',
        WebkitBackdropFilter: 'blur(6px)',
        display: 'flex',
        alignItems: isMobile ? 'flex-end' : 'center',
        justifyContent: 'center',
        padding: isMobile ? 0 : 16,
        animation: `${out ? 'fadeout' : 'fade'} ${
          out ? '0.16s' : '0.18s'
        } ease both`,
      }}
    >
      <div
        ref={ref}
        role="dialog"
        aria-modal="true"
        aria-label={title || 'پنجره محاوره‌ای'}
        onMouseDown={(event) => event.stopPropagation()}
        style={{
          width: isMobile ? '100%' : 'min(480px,100%)',
          maxHeight: 'calc(100vh - 32px)',
          overflowY: 'auto',
          background: 'var(--surface-elevated)',
          border: '1px solid var(--border-strong)',
          borderRadius: isMobile
            ? '16px 16px 0 0'
            : 'var(--radius-lg)',
          padding: isMobile
            ? '24px 20px calc(24px + env(safe-area-inset-bottom,0px))'
            : 24,
          boxShadow:
            '0 40px 120px -30px rgba(47,107,255,0.3)',
          animation: `${
            out ? 'popout' : isMobile ? 'sheet' : 'pop'
          } ${
            out ? '0.16s' : '0.24s'
          } cubic-bezier(0.2,0.7,0.2,1) both`,
        }}
      >
        {title && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: 18,
            }}
          >
            <h2
              style={{
                fontSize: 18,
                fontWeight: 600,
                margin: 0,
              }}
            >
              {title}
            </h2>

            <button
              type="button"
              onClick={close}
              aria-label="بستن"
              style={{
                width: 38,
                height: 38,
                display: 'grid',
                placeItems: 'center',
                borderRadius: 'var(--radius)',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                background: 'none',
                border: 'none',
              }}
            >
              <Icon n="x" />
            </button>
          </div>
        )}

        {typeof children === 'function'
          ? children(close)
          : children}
      </div>
    </div>
  );
}

/* ── Toast ── */
export type ToastItem = {
  id: number;
  title: string;
  detail?: string;
  kind?: string;
};

export function ToastList({
  toasts,
}: {
  toasts: ToastItem[];
}) {
  const colors: Record<string, string> = {
    success: 'var(--success)',
    error: 'var(--danger)',
    info: 'var(--accent-blue)',
  };

  return (
    <div
      style={{
        position: 'fixed',
        zIndex: 200,
        insetInlineStart: 20,
        bottom: 20,
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
        pointerEvents: 'none',
      }}
      aria-live="polite"
      aria-atomic="false"
    >
      {toasts.map((t) => (
        <div
          key={t.id}
          role="status"
          style={{
            background: 'var(--surface-elevated)',
            border: '1px solid var(--border-strong)',
            borderRadius: 8,
            padding: '12px 16px',
            minWidth: 240,
            boxShadow: '0 20px 60px -20px #000',
            animation:
              'toastin 0.32s cubic-bezier(0.2,0.7,0.2,1) both',
            display: 'flex',
            gap: 12,
            alignItems: 'flex-start',
          }}
        >
          <div
            style={{
              color:
                colors[t.kind || 'success'] || colors.success,
              marginTop: 2,
              flexShrink: 0,
            }}
          >
            <Icon
              n={
                t.kind === 'error'
                  ? 'x'
                  : t.kind === 'info'
                    ? 'info'
                    : 'check'
              }
              s={18}
            />
          </div>

          <div>
            <div style={{ fontWeight: 500 }}>
              {t.title}
            </div>

            {t.detail && (
              <div
                style={{
                  color: 'var(--text-secondary)',
                  fontSize: 13,
                  marginTop: 2,
                }}
              >
                {t.detail}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

/* ── Dropdown ── */
export function Dropdown({
  trigger,
  children,
}: {
  trigger: React.ReactNode;
  children: (close: () => void) => React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const close = useCallback(() => {
    setOpen(false);
  }, []);

  useEffect(() => {
    if (!open) return;

    const handleOutsideMouseDown = (
      event: MouseEvent
    ) => {
      if (
        ref.current &&
        !ref.current.contains(event.target as Node)
      ) {
        setOpen(false);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    window.addEventListener(
      'mousedown',
      handleOutsideMouseDown
    );
    window.addEventListener('keydown', handleEscape);

    return () => {
      window.removeEventListener(
        'mousedown',
        handleOutsideMouseDown
      );
      window.removeEventListener(
        'keydown',
        handleEscape
      );
    };
  }, [open]);

  return (
    <div
      style={{ position: 'relative' }}
      ref={ref}
    >
      <button
        type="button"
        onClick={() => setOpen((previous) => !previous)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="بیشتر"
        style={{
          width: 38,
          height: 38,
          display: 'grid',
          placeItems: 'center',
          borderRadius: 'var(--radius)',
          color: 'var(--text-secondary)',
          cursor: 'pointer',
          background: 'none',
          border: 'none',
        }}
      >
        {trigger}
      </button>

      {open && (
        <div
          role="menu"
          style={{
            position: 'absolute',
            insetInlineEnd: 0,
            top: 'calc(100% + 8px)',
            minWidth: 220,
            background: 'var(--surface-elevated)',
            border: '1px solid var(--border-strong)',
            borderRadius: 8,
            padding: 6,
            zIndex: 60,
            animation:
              'pop 0.18s cubic-bezier(0.2,0.7,0.2,1) both',
            boxShadow: '0 30px 80px -20px #000',
          }}
        >
          {children(close)}
        </div>
      )}
    </div>
  );
}

/* ── Dropdown Item ── */
export function DropdownItem({
  onClick,
  icon,
  danger,
  children,
}: {
  onClick: () => void;
  icon?: string;
  danger?: boolean;
  children: React.ReactNode;
}) {
  const [hovered, setHovered] = useState(false);

  return (
    <button
      type="button"
      role="menuitem"
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: 'flex',
        width: '100%',
        textAlign: 'start',
        padding: '10px 12px',
        borderRadius: 6,
        fontSize: 14,
        color: danger
          ? 'var(--danger)'
          : hovered
            ? 'var(--text-primary)'
            : 'var(--text-secondary)',
        gap: 10,
        alignItems: 'center',
        cursor: 'pointer',
        transition: 'background 0.15s, color 0.15s',
        background: hovered
          ? 'rgba(255,255,255,0.06)'
          : 'none',
        border: 'none',
      }}
    >
      {icon && <Icon n={icon} s={16} />}
      {children}
    </button>
  );
}

/* ── Alert Banner ── */
export function AlertBanner({
  alerts,
}: {
  alerts: string[];
}) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed || alerts.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        background: 'rgba(230,180,80,0.1)',
        border: '1px solid rgba(230,180,80,0.3)',
        borderRadius: 'var(--radius)',
        padding: '10px 16px',
        marginBottom: 16,
        display: 'flex',
        gap: 10,
        alignItems: 'flex-start',
      }}
      role="status"
    >
      <span
        style={{
          color: 'var(--warning)',
          flexShrink: 0,
          marginTop: 2,
        }}
      >
        <Icon n="warning" s={18} />
      </span>

      <div
        style={{
          flex: 1,
          fontSize: 13.5,
          color: 'var(--warning)',
        }}
      >
        {alerts.map((alert, index) => (
          <div key={`${index}-${alert}`}>
            {alert}
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={() => setDismissed(true)}
        aria-label="بستن هشدار"
        style={{
          color: 'var(--text-tertiary)',
          flexShrink: 0,
          background: 'none',
          border: 'none',
          cursor: 'pointer',
        }}
      >
        <Icon n="x" s={16} />
      </button>
    </div>
  );
}

/* ── Progress Bar ── */
export function ProgressBar({
  pct,
  color = 'var(--accent-blue)',
  height = 6,
}: {
  pct: number;
  color?: string;
  height?: number;
}) {
  const safePct = Number.isFinite(pct)
    ? Math.min(100, Math.max(0, pct))
    : 0;

  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={safePct}
      style={{
        height,
        background: 'rgba(255,255,255,0.08)',
        borderRadius: height / 2,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: `${safePct}%`,
          height: '100%',
          background:
            safePct >= 100
              ? 'var(--danger)'
              : safePct >= 80
                ? 'var(--warning)'
                : color,
          borderRadius: height / 2,
          transformOrigin: 'right',
          animation:
            'grow 0.9s cubic-bezier(0.2,0.7,0.2,1) both',
          transition: 'width 0.5s',
        }}
      />
    </div>
  );
}

/* ── Segmented Control ── */
export function Seg({
  options,
  value,
  onChange,
}: {
  options: [string, string][];
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div
      style={{
        display: 'inline-flex',
        padding: 3,
        border: '1px solid var(--border)',
        borderRadius: 8,
        background: 'rgba(255,255,255,0.02)',
        gap: 2,
        maxWidth: '100%',
        overflowX: 'auto',
      }}
      role="group"
    >
      {options.map(([optionValue, label]) => {
        const selected = value === optionValue;

        return (
          <button
            key={optionValue}
            type="button"
            onClick={() => onChange(optionValue)}
            aria-pressed={selected}
            style={{
              height: 32,
              padding: '0 13px',
              borderRadius: 6,
              fontSize: 13,
              color: selected
                ? 'var(--text-primary)'
                : 'var(--text-secondary)',
              background: selected
                ? 'var(--surface-hover)'
                : 'none',
              border: selected
                ? '1px solid var(--border-strong)'
                : '1px solid transparent',
              boxShadow: selected
                ? '0 0 0 1px var(--border-strong) inset'
                : 'none',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition:
                'background 0.15s, color 0.15s',
              fontFamily: 'inherit',
            }}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
