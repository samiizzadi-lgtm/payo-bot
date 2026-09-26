import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';

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

/*
 * The website's existing UI is mostly Persian. Instead of forcing every
 * component to be rewritten at once, this layer also translates visible
 * Persian UI text/attributes while English mode is active.
 *
 * It is deliberately local/offline: no third-party translation service is
 * called, and user-entered transaction names are not guessed/rewritten.
 */

const PHRASES: Record<string, string> = {
  'مشکلی پیش آمد.': 'Something went wrong.',
  'اطلاعات مالی‌ات بارگذاری نشد.': 'Your financial data could not be loaded.',
  'لطفاً دوباره تلاش کن.': 'Please try again.',
  'موجودی فعلی': 'Current balance',
  'درآمد ۳۰ روز': 'Income · 30 days',
  'هزینه‌ها ۳۰ روز': 'Expenses · 30 days',
  'پس‌انداز ۳۰ روز': 'Savings · 30 days',
  'از درآمد': 'of income',
  'نسبت به ماه قبل': 'vs. last month',
  'ثبت هزینه': 'Add expense',
  'ثبت درآمد': 'Add income',
  'آخرین تراکنش‌ها': 'Recent transactions',
  'هنوز تراکنشی نیست.': 'No transactions yet.',
  'اولین درآمد یا هزینه‌ات را ثبت کن.': 'Add your first income or expense.',
  'ثبت تراکنش': 'Add transaction',
  'تراکنش‌ها بارگذاری نشدند.': 'Transactions could not be loaded.',
  'دسته‌بندی‌ها بارگذاری نشدند.': 'Categories could not be loaded.',
  'هنوز هزینه‌ای ثبت نشده.': 'No expenses recorded yet.',
  'هزینه‌ها · ۳۰ روز': 'Expenses · 30 days',
  'بستن فیلترهای بیشتر': 'Hide more filters',
  'فیلترهای بیشتر': 'More filters',
  'حذف همه فیلترها': 'Clear all filters',
  'تا تاریخ': 'To date',
  'از تاریخ': 'From date',
  'حداقل مبلغ (تومان)': 'Minimum amount (Toman)',
  'حداکثر مبلغ (تومان)': 'Maximum amount (Toman)',
  'مثلاً': 'e.g.',
  'تاریخ': 'Date',
  'نام': 'Name',
  'دسته': 'Category',
  'نوع': 'Type',
  'مبلغ': 'Amount',
  'وضعیت': 'Status',
  'انجام‌شده': 'Completed',
  'در انتظار': 'Pending',
  'درآمد': 'Income',
  'هزینه': 'Expense',
  'بودجه ذخیره شد': 'Budget saved',
  'مدیریت مالی': 'Financial management',
  'بودجه‌ی ماهانه': 'Monthly budget',
  'سقف هزینه‌ها را تنظیم کن و مصرف هر دسته را در همین صفحه ببین.':
    'Set spending limits and view category usage on this page.',
  'کل بودجه': 'Total budget',
  'مصرف‌شده': 'Spent',
  'باقی‌مانده': 'Remaining',
  'ذخیره': 'Save',
  'افزودن': 'Add',
  'افزودن بودجه': 'Add budget',
  'حذف': 'Delete',
  'ویرایش': 'Edit',
  'بازنشانی': 'Reset',
  'لغو': 'Cancel',
  'تأیید': 'Confirm',
  'بستن': 'Close',
  'بازگشت': 'Back',
  'مرکز بینش': 'Insights center',
  'تحلیل مالی': 'Financial analytics',
  'روند درآمد و هزینه': 'Income and expense trend',
  'در حال به‌روزرسانی…': 'Updating…',
  'یک سال': '1 year',
  '۷ روز': '7 days',
  '۳۰ روز': '30 days',
  '۹۰ روز': '90 days',
  'همه': 'All',
  'روز': 'days',
  'امروز': 'Today',
  'دیروز': 'Yesterday',
  'تاریخ نامعتبر': 'Invalid date',
  'چاپ / PDF': 'Print / PDF',
  'بازنشانی داده‌های نمونه': 'Reset demo data',
  'تغییر زبان': 'Change language',
  'ناوبری': 'Navigation',
  'ثبت': 'Add',
  'CSV': 'CSV',
  'تحلیل': 'Analytics',
  'داشبورد': 'Dashboard',
  'تراکنش‌ها': 'Transactions',
  'بودجه': 'Budget',
  'دسته‌بندی‌ها': 'Categories',
  'پس‌انداز': 'Savings',
  'موجودی': 'Balance',
  'گزارش': 'Report',
  'گزارش مالی': 'Financial report',
  'نمودار': 'Chart',
  'رادار': 'Radar',
  'هدف‌ها': 'Goals',
  'هدف': 'Goal',
  'حافظه': 'Memory',
  'هوش مصنوعی': 'AI',
  'تنظیمات': 'Settings',
  'راهنما': 'Help',
  'درباره پایو': 'About Payo',
  'درباره Payo': 'About Payo',
  'زبان': 'Language',
  'درآمدها': 'Income',
  'هزینه‌ها': 'Expenses',
  'ثبت نشده': 'Not recorded',
  'در حال بارگذاری…': 'Loading…',
  'در حال بارگذاری': 'Loading',
  'دوباره تلاش کن': 'Try again',
  'اطلاعات': 'Data',
  'مالی': 'Financial',
  'ماه قبل': 'last month',
  'این ماه': 'this month',
  'هفته': 'week',
  'ماه': 'month',
  'سال': 'year',
  'روزانه': 'Daily',
  'هفتگی': 'Weekly',
  'ماهانه': 'Monthly',
  'سالانه': 'Yearly',
  'دوره': 'Period',
  'مقایسه': 'Comparison',
  'حالت مقایسه': 'Comparison mode',
  'حالت عادی': 'Normal mode',
};

const WORDS: Record<string, string> = {
  'مشکلی': 'Something',
  'پیش': 'happened',
  'آمد': 'came',
  'اطلاعات': 'data',
  'مالی‌ات': 'financial',
  'مالی': 'financial',
  'بارگذاری': 'loading',
  'نشد': 'failed',
  'نشده': 'not recorded',
  'لطفاً': 'Please',
  'دوباره': 'again',
  'تلاش': 'try',
  'کن': 'try',
  'موجودی': 'Balance',
  'فعلی': 'current',
  'درآمد': 'Income',
  'درآمدها': 'Income',
  'هزینه': 'Expense',
  'هزینه‌ها': 'Expenses',
  'پس‌انداز': 'Savings',
  'از': 'of',
  'نسبت': 'vs.',
  'به': 'to',
  'ماه': 'month',
  'قبل': 'last',
  'آخرین': 'Recent',
  'تراکنش': 'transaction',
  'تراکنش‌ها': 'transactions',
  'هنوز': 'No',
  'اولین': 'first',
  'ثبت': 'Add',
  'دسته': 'Category',
  'دسته‌بندی': 'Category',
  'دسته‌بندی‌ها': 'Categories',
  'هزینه‌ای': 'expense',
  'تا': 'to',
  'تاریخ': 'date',
  'حداقل': 'Minimum',
  'حداکثر': 'Maximum',
  'مبلغ': 'Amount',
  'مثلاً': 'e.g.',
  'فیلترها': 'filters',
  'فیلترهای': 'filters',
  'بیشتر': 'more',
  'بستن': 'Hide',
  'حذف': 'Delete',
  'همه': 'All',
  'وضعیت': 'Status',
  'نوع': 'Type',
  'نام': 'Name',
  'انجام‌شده': 'Completed',
  'در': 'In',
  'انتظار': 'Pending',
  'مدیریت': 'Management',
  'بودجه': 'Budget',
  'بودجه‌ی': 'Budget',
  'ماهانه': 'Monthly',
  'کل': 'Total',
  'مصرف‌شده': 'Spent',
  'باقی‌مانده': 'Remaining',
  'تنظیم': 'Set',
  'ذخیره': 'Save',
  'ذخیره‌شده': 'Saved',
  'ذخیره': 'Save',
  'مرکز': 'Center',
  'بینش': 'Insights',
  'تحلیل': 'Analytics',
  'مالی': 'Financial',
  'روند': 'Trend',
  'به‌روزرسانی': 'Updating',
  'یک': '1',
  'سال': 'year',
  'روز': 'days',
  'امروز': 'Today',
  'دیروز': 'Yesterday',
  'نامعتبر': 'Invalid',
  'چاپ': 'Print',
  'بازنشانی': 'Reset',
  'داده‌های': 'data',
  'نمونه': 'demo',
  'تغییر': 'Change',
  'زبان': 'Language',
  'ناوبری': 'Navigation',
  'گزارش': 'Report',
  'نمودار': 'Chart',
  'رادار': 'Radar',
  'هدف': 'Goal',
  'هدف‌ها': 'Goals',
  'حافظه': 'Memory',
  'هوش': 'AI',
  'مصنوعی': 'AI',
  'تنظیمات': 'Settings',
  'راهنما': 'Help',
  'درباره': 'About',
  'پایو': 'Payo',
  'قبض': 'Bill',
  'قبوض': 'Bills',
  'خرید': 'Shopping',
  'غذا': 'Food',
  'حمل‌ونقل': 'Transportation',
  'تفریح': 'Entertainment',
  'سلامت': 'Health',
  'سایر': 'Other',
  'سایر‌درآمدها': 'Other income',
  'سایر درآمدها': 'Other income',
  'حقوق': 'Salary',
  'فریلنس': 'Freelance',
  'اسنپ': 'Snapp',
  'تپسی': 'Tapsi',
  'بنزین': 'Fuel',
  'مترو': 'Metro',
  'رستوران': 'Restaurant',
  'کافه': 'Cafe',
  'اسنپ‌فود': 'Snappfood',
  'سوپر': 'Grocery',
  'نانوایی': 'Bakery',
  'دیجی': 'Digikala',
  'پوشاک': 'Clothing',
  'لباس': 'Clothes',
  'برق': 'Electricity',
  'گاز': 'Gas',
  'اینترنت': 'Internet',
  'آب': 'Water',
  'سینما': 'Cinema',
  'نتفلیکس': 'Netflix',
  'بازی': 'Gaming',
  'دارو': 'Medicine',
  'داروخانه': 'Pharmacy',
  'پزشک': 'Doctor',
  'بیمارستان': 'Hospital',
  'پروژه': 'Project',
  'سقف': 'Limit',
  'به‌روزرسانی': 'updated',
  'شد': 'was',
  'شده': 'done',
  'مصرف': 'Usage',
  'تنظیمات': 'Settings',
};

const normalize = (value: string) =>
  value.replace(/\u064a/g, 'ی').replace(/\u0643/g, 'ک').trim();

const containsPersian = (value: string) =>
  /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/.test(
    value,
  );

const latinizeDigits = (value: string) =>
  value
    .replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d)))
    .replace(/[٠-٩]/g, (d) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(d)))
    .replace(/٪/g, '%')
    .replace(/[«»]/g, '"');

function translatePersianText(value: string): string {
  let text = latinizeDigits(value);
  const exact = PHRASES[normalize(text)];
  if (exact) return exact;

  text = text.replace(
    /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+/g,
    (token) => WORDS[normalize(token)] ?? token,
  );

  text = text.replace(/\s*·\s*/g, ' · ');
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

function translateElementAttributes(
  element: HTMLElement,
  english: boolean,
  originals: WeakMap<HTMLElement, Record<string, string>>,
) {
  const attrs = ['placeholder', 'title', 'aria-label', 'aria-description'];

  for (const attr of attrs) {
    const current = element.getAttribute(attr);
    if (current == null) continue;

    if (!originals.has(element)) originals.set(element, {});
    const store = originals.get(element)!;

    if (store[attr] == null && containsPersian(current)) {
      store[attr] = current;
    }

    const original = store[attr] ?? current;

    if (english) {
      if (containsPersian(original)) {
        element.setAttribute(attr, translatePersianText(original));
      }
    } else if (store[attr] != null) {
      element.setAttribute(attr, store[attr]);
    }
  }
}

function createDocumentTranslator() {
  const textOriginals = new WeakMap<Text, string>();
  const elementOriginals = new WeakMap<HTMLElement, Record<string, string>>();
  let english = false;

  const skip = (node: Node) => {
    const parent = node.parentElement;
    if (!parent) return false;
    return !!parent.closest(
      'script,style,noscript,code,pre,svg,[data-payo-no-i18n]',
    );
  };

  const translateTextNode = (node: Text) => {
    if (skip(node)) return;

    const current = node.nodeValue ?? '';
    if (!textOriginals.has(node) && containsPersian(current)) {
      textOriginals.set(node, current);
    }

    const original = textOriginals.get(node);
    if (original == null) return;

    const next = english ? translatePersianText(original) : original;
    if (node.nodeValue !== next) {
      node.nodeValue = next;
    }
  };

  const scan = () => {
    if (typeof document === 'undefined') return;

    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
    );
    let node: Node | null;

    while ((node = walker.nextNode())) {
      translateTextNode(node as Text);
    }

    document.querySelectorAll<HTMLElement>('*').forEach((element) => {
      translateElementAttributes(element, english, elementOriginals);
    });
  };

  let observer: MutationObserver | null = null;

  const start = () => {
    if (typeof document === 'undefined') return;
    scan();

    observer?.disconnect();
    observer = new MutationObserver(() => {
      scan();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ['placeholder', 'title', 'aria-label', 'aria-description'],
    });
  };

  return {
    setLanguage(nextLanguage: Language) {
      english = nextLanguage === 'en';
      scan();
    },
    start,
  };
}

const docTranslator =
  typeof window !== 'undefined' ? createDocumentTranslator() : null;

function readStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'fa';
  return window.localStorage.getItem(STORAGE_KEY) === 'en' ? 'en' : 'fa';
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

  document.documentElement.dataset.payoLanguage = language;
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>(readStoredLanguage);
  const initialized = useRef(false);

  const setLanguage = (next: Language) => {
    setLanguageState(next);
    window.localStorage.setItem(STORAGE_KEY, next);
    applyDocumentLanguage(next);
    docTranslator?.setLanguage(next);
  };

  useEffect(() => {
    applyDocumentLanguage(language);

    if (!initialized.current) {
      docTranslator?.start();
      initialized.current = true;
    }

    docTranslator?.setLanguage(language);
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

  return (
    <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
  );
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
      aria-label={language === 'fa' ? 'زبان' : 'Language'}
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

