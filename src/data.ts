export type TxType = 'income' | 'expense';
export type TxStatus = 'completed' | 'pending';
export type TxSource = 'web' | 'telegram';

export interface Transaction {
  id: string;
  date: string; // YYYY-MM-DD
  name: string;
  category: string;
  amount: number; // Toman
  type: TxType;
  status: TxStatus;
  source: TxSource;
}

export interface FinancialSummary {
  balance: number;
  income: number;
  expenses: number;
  savings: number;
  prevIncome: number;
  prevExpenses: number;
  changePct: number;
  trend: number[];
}

export interface SeriesPoint {
  label: string;
  rangeLabel: string;
  income: number;
  expenses: number;
  net: number;
}

export interface CategoryStat {
  category: string;
  amount: number;
  share: number;
  prev: number;
}

export interface Insight {
  id: string;
  text: string;
  type?: 'info' | 'warning' | 'success';
}

export interface BudgetItem {
  category: string;
  limit: number;
}

export interface SavingsGoal {
  id: string;
  name: string;
  target: number;
  current: number;
  deadline?: string;
  color: string;
}

export const EXPENSE_CATEGORIES = [
  'غذا',
  'حمل‌ونقل',
  'خرید',
  'قبوض',
  'تفریح',
  'سلامت',
  'سایر',
];

export const INCOME_CATEGORIES = [
  'حقوق',
  'فریلنس',
  'سایر درآمدها',
];

export const ALL_CATEGORIES = [
  ...EXPENSE_CATEGORIES,
  ...INCOME_CATEGORIES,
];

export const CATEGORY_COLOR: Record<string, string> = {
  غذا: '#2f6bff',
  'حمل‌ونقل': '#5f8dff',
  خرید: '#93b0ff',
  قبوض: '#c3d3ff',
  تفریح: '#7d8698',
  سلامت: '#545c6b',
  سایر: '#3a404c',
  حقوق: '#2f6bff',
  فریلنس: '#5f8dff',
  'سایر درآمدها': '#93b0ff',
};

export const getCategoryColor = (cat: string): string =>
  CATEGORY_COLOR[cat] || '#5f8dff';

export const SMART_CATEGORY_MAP: Record<string, string> = {
  اسنپ: 'حمل‌ونقل',
  تپسی: 'حمل‌ونقل',
  بنزین: 'حمل‌ونقل',
  مترو: 'حمل‌ونقل',

  غذا: 'غذا',
  رستوران: 'غذا',
  کافه: 'غذا',
  'اسنپ‌فود': 'غذا',
  سوپر: 'غذا',
  نانوایی: 'غذا',

  دیجی: 'خرید',
  خرید: 'خرید',
  پوشاک: 'خرید',
  لباس: 'خرید',

  برق: 'قبوض',
  گاز: 'قبوض',
  اینترنت: 'قبوض',
  قبض: 'قبوض',
  آب: 'قبوض',

  سینما: 'تفریح',
  نتفلیکس: 'تفریح',
  بازی: 'تفریح',

  دارو: 'سلامت',
  داروخانه: 'سلامت',
  پزشک: 'سلامت',
  بیمارستان: 'سلامت',

  حقوق: 'حقوق',
  فریلنس: 'فریلنس',
  پروژه: 'فریلنس',
};

export function suggestCategory(
  name: string | null | undefined
): string | null {
  const normalizedName = (name ?? '').trim().toLowerCase();

  if (!normalizedName) {
    return null;
  }

  for (const [keyword, category] of Object.entries(
    SMART_CATEGORY_MAP
  )) {
    if (
      normalizedName.includes(keyword.toLowerCase())
    ) {
      return category;
    }
  }

  return null;
}

export const RANGES = [
  { id: '7d', label: '۷ روز', days: 7, n: 7 },
  { id: '30d', label: '۳۰ روز', days: 30, n: 10 },
  { id: '3m', label: '۳ ماه', days: 90, n: 13 },
  { id: '6m', label: '۶ ماه', days: 180, n: 12 },
  { id: '1y', label: '۱ سال', days: 365, n: 12 },
];

export const TARGET_BALANCE = 48250000;
export const DEMO_CHANGE_PCT = 8.4;

export const CRAFTED: [
  number,
  string,
  string,
  number,
  TxType?,
  TxStatus?
][] = [
  [17, 'حقوق ماهانه', 'حقوق', 14000000, 'income'],
  [9, 'پروژه فریلنسری', 'فریلنس', 3500000, 'income'],
  [4, 'بازگشت وجه', 'سایر درآمدها', 1000000, 'income'],

  [0, 'اسنپ‌فود', 'غذا', 385000],
  [2, 'کافه', 'غذا', 210000],
  [3, 'سوپرمارکت', 'غذا', 1240000],
  [6, 'رستوران', 'غذا', 760000],
  [11, 'نانوایی و میوه', 'غذا', 180000],

  [1, 'اسنپ', 'حمل‌ونقل', 145000],
  [5, 'تپسی', 'حمل‌ونقل', 98000],
  [8, 'بنزین', 'حمل‌ونقل', 400000],
  [14, 'مترو', 'حمل‌ونقل', 60000],

  [1, 'دیجی‌کالا', 'خرید', 900000, 'expense', 'pending'],
  [12, 'پوشاک', 'خرید', 980000],

  [20, 'قبض برق', 'قبوض', 420000],
  [19, 'قبض گاز', 'قبوض', 310000],
  [23, 'اینترنت', 'قبوض', 690000],

  [7, 'سینما', 'تفریح', 280000],
  [13, 'اشتراک نتفلیکس', 'تفریح', 450000],

  [10, 'داروخانه', 'سلامت', 340000],
];

export const MERCHANTS: Record<
  string,
  [string, number, number][]
> = {
  غذا: [
    ['اسنپ‌فود', 250, 600],
    ['رستوران', 400, 1100],
    ['سوپرمارکت', 300, 1400],
    ['کافه', 120, 320],
  ],
  'حمل‌ونقل': [
    ['اسنپ', 70, 260],
    ['تپسی', 60, 220],
    ['بنزین', 250, 500],
  ],
  خرید: [
    ['دیجی‌کالا', 400, 3200],
    ['پوشاک', 500, 1800],
  ],
  تفریح: [
    ['سینما', 200, 400],
    ['کافه بازی', 150, 600],
  ],
  سلامت: [['داروخانه', 100, 600]],
  سایر: [
    ['هدیه', 200, 900],
    ['متفرقه', 60, 400],
  ],
};

export const DEFAULT_BUDGETS: BudgetItem[] = [
  { category: 'غذا', limit: 3000000 },
  { category: 'حمل‌ونقل', limit: 1000000 },
  { category: 'خرید', limit: 2000000 },
  { category: 'قبوض', limit: 1500000 },
  { category: 'تفریح', limit: 1000000 },
  { category: 'سلامت', limit: 800000 },
];

export const DEFAULT_GOALS: SavingsGoal[] = [
  {
    id: 'g1',
    name: 'صندوق اضطراری',
    target: 30000000,
    current: 12500000,
    color: '#2f6bff',
  },
  {
    id: 'g2',
    name: 'سفر نوروز',
    target: 10000000,
    current: 4200000,
    deadline: '2026-03-20',
    color: '#5f8dff',
  },
  {
    id: 'g3',
    name: 'لپ‌تاپ جدید',
    target: 25000000,
    current: 8000000,
    color: '#93b0ff',
  },
];
