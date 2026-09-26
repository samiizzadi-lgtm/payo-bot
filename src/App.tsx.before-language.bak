import React, { useEffect } from 'react';
import { StoreProvider, useStore } from './store';
import { useRoute } from './components/hooks';
import {
  Icon,
  Logo,
  ToastList,
  Dropdown,
  DropdownItem,
} from './components/ui';
import { Dashboard } from './pages/Dashboard';
import { Transactions } from './pages/Transactions';
import { Analytics } from './pages/Analytics';
import { Budget } from './pages/Budget';
import { AddModal, DetailModal } from './components/Modals';
import { api } from './mock';

const NAV: [string, string, string][] = [
  ['/', 'داشبورد', 'home'],
  ['/tx', 'تراکنش‌ها', 'list'],
  ['/stats', 'تحلیل', 'chart'],
  ['/budget', 'بودجه', 'wallet'],
];

function AppShell() {
  const route = useRoute();
  const { modal, closeModal, openAdd, toasts } = useStore();
  const path = route.path;

  useEffect(() => {
    document.title = 'Payo';
  }, []);

  const isActive = (p: string) =>
    p === '/'
      ? path !== '/tx' && path !== '/stats' && path !== '/budget'
      : path === p;

  const Page =
    path === '/tx' ? (
      <Transactions key="tx" query={route.query} />
    ) : path === '/stats' ? (
      <Analytics key="st" />
    ) : path === '/budget' ? (
      <Budget key="bg" />
    ) : (
      <Dashboard key="db" />
    );

  const topbarStyle: React.CSSProperties = {
    position: 'sticky',
    top: 'env(safe-area-inset-top, 0px)',
    zIndex: 40,
    background: 'rgba(0,0,0,0.76)',
    backdropFilter: 'blur(16px)',
    WebkitBackdropFilter: 'blur(16px)',
    borderBottom: '1px solid var(--border)',
  };

  const navLinkBase: React.CSSProperties = {
    position: 'relative',
    padding: '8px 14px',
    fontSize: 14,
    borderRadius: 'var(--radius)',
    transition: 'color 0.15s',
    textDecoration: 'none',
    cursor: 'pointer',
  };

  return (
    <>
      {/* Splash */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: 300,
          background: '#000',
          display: 'grid',
          placeItems: 'center',
          animation: 'splashout 0.5s ease 0.7s both',
          pointerEvents: 'none',
        }}
        aria-hidden="true"
      >
        <Logo size={32} />
      </div>

      {/* Topbar */}
      <header style={topbarStyle} className="no-print">
        <div
          style={{
            maxWidth: 1180,
            margin: '0 auto',
            height: 60,
            padding: '0 20px',
            display: 'flex',
            alignItems: 'center',
            gap: 28,
          }}
        >
          <a href="#/" aria-label="Payo">
            <Logo />
          </a>

          {/* Desktop navigation */}
          <nav style={{ display: 'flex', gap: 4, flex: 1 }}>
            {NAV.map(([p, label]) => (
              <a
                key={p}
                href={'#' + p}
                aria-current={isActive(p) ? 'page' : undefined}
                style={{
                  ...navLinkBase,
                  color: isActive(p)
                    ? 'var(--text-primary)'
                    : 'var(--text-secondary)',
                }}
              >
                {isActive(p) && (
                  <span
                    style={{
                      position: 'absolute',
                      insetInline: 14,
                      bottom: -13,
                      height: 2,
                      background: 'var(--accent-blue)',
                      boxShadow: '0 0 12px var(--accent-glow)',
                      borderRadius: 1,
                    }}
                  />
                )}
                {label}
              </a>
            ))}
          </nav>

          {/* Mobile spacer */}
          <div
            style={{ flex: 1, display: 'none' }}
            className="only-m"
          />

          <button
            type="button"
            onClick={() => openAdd('expense')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              height: 36,
              padding: '0 14px',
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

          <Dropdown trigger={<Icon n="more" />}>
            {(close) => (
              <>
                <DropdownItem
                  icon="download"
                  onClick={() => {
                    close();
                    window.print();
                  }}
                >
                  چاپ / PDF
                </DropdownItem>

                <DropdownItem
                  icon="trash"
                  onClick={() => {
                    close();
                    api.reset();
                    window.location.reload();
                  }}
                  danger
                >
                  بازنشانی داده‌های نمونه
                </DropdownItem>
              </>
            )}
          </Dropdown>
        </div>
      </header>

      <main>{Page}</main>

      {/* Bottom navigation (mobile) */}
      <nav
        className="no-print"
        style={{
          display: 'none',
          gridTemplateColumns: `repeat(${NAV.length},1fr)`,
          position: 'fixed',
          insetInline: 0,
          bottom: 0,
          zIndex: 50,
          background: 'rgba(6,7,9,0.94)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderTop: '1px solid var(--border)',
          padding:
            '8px 8px calc(8px + env(safe-area-inset-bottom,0px))',
        }}
        aria-label="ناوبری"
      >
        {NAV.map(([p, label, icon]) => (
          <a
            key={p}
            href={'#' + p}
            aria-current={isActive(p) ? 'page' : undefined}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
              padding: '6px 0',
              fontSize: 11,
              lineHeight: 1.5,
              color: isActive(p)
                ? 'var(--text-primary)'
                : 'var(--text-tertiary)',
              textDecoration: 'none',
            }}
          >
            <span
              style={{
                color: isActive(p)
                  ? 'var(--accent-blue)'
                  : 'inherit',
              }}
            >
              <Icon n={icon} s={22} />
            </span>
            {label}
          </a>
        ))}
      </nav>

      {/* Floating action button (mobile) */}
      <button
        type="button"
        onClick={() => openAdd('expense')}
        className="no-print"
        style={{
          position: 'fixed',
          insetInlineStart: 16,
          bottom: 'calc(84px + env(safe-area-inset-bottom,0px))',
          zIndex: 45,
          width: 54,
          height: 54,
          borderRadius: 14,
          background: 'var(--accent-blue)',
          display: 'none',
          placeItems: 'center',
          boxShadow: '0 14px 40px -8px var(--accent-glow)',
          border: 'none',
          cursor: 'pointer',
          color: 'white',
        }}
        aria-label="ثبت تراکنش"
      >
        <Icon n="plus" s={26} />
      </button>

      {/* Modals */}
      {modal?.kind === 'add' && (
        <AddModal
          defaults={{ type: modal.type }}
          onClose={closeModal}
        />
      )}

      {modal?.kind === 'tx' && (
        <DetailModal
          t={modal.t}
          onClose={closeModal}
        />
      )}

      {/* Toast notifications */}
      <ToastList toasts={toasts} />
    </>
  );
}

export default function App() {
  return (
    <StoreProvider>
      <AppShell />
    </StoreProvider>
  );
}
