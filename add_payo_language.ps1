$ErrorActionPreference = "Stop"

$root = Get-Location
$app = Join-Path $root "src\App.tsx"
$css = Join-Path $root "src\index.css"
$i18n = Join-Path $root "src\i18n.tsx"

if (-not (Test-Path $app)) { throw "src\App.tsx پیدا نشد. این اسکریپت را از ریشه پروژه Payo اجرا کن." }
if (-not (Test-Path $css)) { throw "src\index.css پیدا نشد." }

Copy-Item $app "$app.before-language.bak" -Force
Copy-Item $css "$css.before-language.bak" -Force

$i18nContent = @'
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';

export type Language = 'fa' | 'en';

type I18nContextValue = {
  language: Language;
  isPersian: boolean;
  dir: 'rtl' | 'ltr';
  setLanguage: (language: Language) => void;
  toggleLanguage: () => void;
  t: (fa: string, en: string) => string;
};

const STORAGE_KEY = 'payo-language';

const I18nContext = createContext<I18nContextValue | null>(null);

function readStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'fa';
  const value = window.localStorage.getItem(STORAGE_KEY);
  return value === 'en' ? 'en' : 'fa';
}

function applyDocumentLanguage(language: Language) {
  if (typeof document === 'undefined') return;

  const isPersian = language === 'fa';
  const dir = isPersian ? 'rtl' : 'ltr';

  document.documentElement.lang = isPersian ? 'fa' : 'en';
  document.documentElement.dir = dir;

  document.body.lang = isPersian ? 'fa' : 'en';
  document.body.dir = dir;
  document.body.style.direction = dir;
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>(readStoredLanguage);

  const setLanguage = (next: Language) => {
    setLanguageState(next);
    window.localStorage.setItem(STORAGE_KEY, next);
    applyDocumentLanguage(next);
  };

  useEffect(() => {
    applyDocumentLanguage(language);
  }, [language]);

  const value = useMemo<I18nContextValue>(
    () => ({
      language,
      isPersian: language === 'fa',
      dir: language === 'fa' ? 'rtl' : 'ltr',
      setLanguage,
      toggleLanguage: () => setLanguage(language === 'fa' ? 'en' : 'fa'),
      t: (fa, en) => (language === 'fa' ? fa : en),
    }),
    [language],
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useLanguage() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useLanguage must be used inside LanguageProvider');
  }
  return context;
}

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <div
      className="payo-language-switcher"
      role="group"
      aria-label="Language"
      title={language === 'fa' ? 'تغییر زبان' : 'Change language'}
    >
      <span aria-hidden="true">🌐</span>

      <button
        type="button"
        className={language === 'en' ? 'active' : ''}
        onClick={() => setLanguage('en')}
        aria-pressed={language === 'en'}
      >
        English
      </button>

      <span className="separator" aria-hidden="true">
        |
      </span>

      <button
        type="button"
        className={language === 'fa' ? 'active' : ''}
        onClick={() => setLanguage('fa')}
        aria-pressed={language === 'fa'}
      >
        فارسی
      </button>
    </div>
  );
}

'@
Set-Content -Path $i18n -Value $i18nContent -Encoding UTF8

$appContent = @'
﻿import React, { useEffect } from 'react';
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
import { LanguageProvider, LanguageSwitcher, useLanguage } from './i18n';

function AppShell() {
  const route = useRoute();
  const { modal, closeModal, openAdd, toasts } = useStore();
  const { t } = useLanguage();
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

  const navItems: [string, string, string][] = [
    ['/', t('داشبورد', 'Dashboard'), 'home'],
    ['/tx', t('تراکنش‌ها', 'Transactions'), 'list'],
    ['/stats', t('تحلیل', 'Analytics'), 'chart'],
    ['/budget', t('بودجه', 'Budget'), 'wallet'],
  ];

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
            gap: 16,
          }}
        >
          <a href="#/" aria-label="Payo">
            <Logo />
          </a>

          {/* Desktop navigation */}
          <nav style={{ display: 'flex', gap: 4, flex: 1 }}>
            {navItems.map(([p, label]) => (
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

          {/* Language switcher */}
          <LanguageSwitcher />

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
            {t('ثبت', 'Add')}
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
                  {t('چاپ / PDF', 'Print / PDF')}
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
                  {t('بازنشانی داده‌های نمونه', 'Reset demo data')}
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
          gridTemplateColumns: `repeat(${navItems.length},1fr)`,
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
        aria-label={t('ناوبری', 'Navigation')}
      >
        {navItems.map(([p, label, icon]) => (
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
        aria-label={t('ثبت تراکنش', 'Add transaction')}
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
    <LanguageProvider>
      <StoreProvider>
        <AppShell />
      </StoreProvider>
    </LanguageProvider>
  );
}

'@
Set-Content -Path $app -Value $appContent -Encoding UTF8

Add-Content -Path $css -Value @'


/* Payo bilingual language switcher */
.payo-language-switcher {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 34px;
  padding: 4px 8px;
  border: 1px solid var(--border-strong);
  border-radius: 999px;
  background: rgba(255,255,255,.035);
  color: var(--text-secondary);
  white-space: nowrap;
  direction: ltr;
  flex-shrink: 0;
}

.payo-language-switcher button {
  border: 0;
  padding: 4px 6px;
  border-radius: 999px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}

.payo-language-switcher button.active {
  background: var(--accent-soft);
  color: var(--text-primary);
}

.payo-language-switcher .separator {
  opacity: .45;
}

html[dir="ltr"] body {
  direction: ltr;
}

html[dir="rtl"] body {
  direction: rtl;
}

@media (max-width: 760px) {
  .payo-language-switcher {
    order: 2;
    margin-inline-start: auto;
  }

  header > div {
    gap: 8px !important;
  }

  .payo-language-switcher button {
    font-size: 11px;
  }
}

'@

Write-Host ""
Write-Host "Payo language switcher added successfully." -ForegroundColor Green
Write-Host "Created: src\i18n.tsx"
Write-Host "Updated: src\App.tsx"
Write-Host "Updated: src\index.css"
Write-Host ""
Write-Host "Backup files:"
Write-Host "  src\App.tsx.before-language.bak"
Write-Host "  src\index.css.before-language.bak"
Write-Host ""
Write-Host "Next: npm run build"
