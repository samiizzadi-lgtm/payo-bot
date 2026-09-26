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

