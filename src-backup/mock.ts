import {
  Transaction, FinancialSummary, SeriesPoint, CategoryStat, Insight,
  BudgetItem, SavingsGoal,
  CRAFTED, MERCHANTS, RANGES,
  TARGET_BALANCE, DEMO_CHANGE_PCT, DEFAULT_BUDGETS, DEFAULT_GOALS,
} from './data';
import { iso, today0, addDays, daysAgo, toman, fa, F, predictNext } from './utils';

const net = (t: Transaction) => (t.type === 'income' ? t.amount : -t.amount);
const idn = (t: Transaction) => Number(String(t.id).replace(/\D/g, '')) || 0;

const mulberry = (a: number) => () => {
  a |= 0;
  a = (a + 0x6D2B79F5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

function seed() {
  const rnd = mulberry(11);
  const T = today0();
  const out: Transaction[] = [];
  let id = 1;

  const add = (
    off: number,
    name: string,
    category: string,
    amount: number,
    type: 'income' | 'expense' = 'expense',
    status: 'completed' | 'pending' = 'completed',
  ) => out.push({
    id: 't' + id++,
    date: iso(addDays(T, -off)),
    name,
    category,
    amount,
    type,
    status,
    source: 'web',
  });

  CRAFTED.forEach((c) =>
    add(c[0], c[1], c[2], c[3], c[4] || 'expense', c[5] || 'completed'),
  );

  const craftedExpenses = CRAFTED
    .filter((c) => (c[4] || 'expense') === 'expense')
    .reduce((a, c) => a + c[3], 0);

  add(15, 'هدیه', 'سایر', 8120000 - craftedExpenses);

  for (let k = 1; k <= 12; k++) {
    add(17 + 30 * k, 'حقوق ماهانه', 'حقوق', 14000000, 'income');

    if (rnd() < 0.45) {
      add(
        9 + 30 * k,
        'پروژه فریلنسری',
        'فریلنس',
        Math.round((2 + rnd() * 3) * 10) * 100000,
        'income',
      );
    }

    add(20 + 30 * k, 'قبض برق', 'قبوض', 380000 + Math.round(rnd() * 8) * 10000);
    add(23 + 30 * k, 'اینترنت', 'قبوض', 690000);
    add(13 + 30 * k, 'اشتراک نتفلیکس', 'تفریح', 450000);
  }

  const bag = ['غذا', 'غذا', 'غذا', 'حمل‌ونقل', 'حمل‌ونقل', 'خرید', 'تفریح', 'سلامت', 'سایر'];

  for (let off = 30; off < 400; off++) {
    if (rnd() < 0.38) {
      const cat = bag[Math.floor(rnd() * bag.length)];
      const list = MERCHANTS[cat] || MERCHANTS['سایر'];
      const m = list[Math.floor(rnd() * list.length)];

      add(
        off,
        m[0],
        cat,
        Math.max(1, Math.round((m[1] + rnd() * (m[2] - m[1])) / 10)) * 10000,
      );
    }
  }

  const opening = TARGET_BALANCE - out.reduce((a, t) => a + net(t), 0);
  return { txns: out, opening, next: id };
}

interface DB {
  txns: Transaction[];
  opening: number;
  next: number;
  budgets: BudgetItem[];
  goals: SavingsGoal[];
}

const KEY = 'payo.v2';

const loadDb = (): DB | null => {
  try {
    const s = localStorage.getItem(KEY);
    if (s) return JSON.parse(s) as DB;
  } catch {
    // Ignore invalid local storage data.
  }
  return null;
};

const saveDb = (db: DB) => {
  try {
    localStorage.setItem(KEY, JSON.stringify(db));
  } catch {
    // Storage may be unavailable or full.
  }
};

let db: DB = (() => {
  const saved = loadDb();

  if (
    saved &&
    Array.isArray(saved.txns) &&
    Array.isArray(saved.budgets) &&
    Array.isArray(saved.goals) &&
    typeof saved.opening === 'number' &&
    typeof saved.next === 'number'
  ) {
    return saved;
  }

  const { txns, opening, next } = seed();
  return { txns, opening, next, budgets: DEFAULT_BUDGETS, goals: DEFAULT_GOALS };
})();

const sorted = () =>
  db.txns.slice().sort((a, b) => b.date.localeCompare(a.date) || idn(b) - idn(a));

const sumWin = (from: number, to: number, type?: string) =>
  db.txns
    .filter((t) => {
      const o = daysAgo(t.date);
      return o >= from && o < to && (!type || t.type === type);
    })
    .reduce((a, t) => a + t.amount, 0);

const rangeOf = (id: string) => RANGES.find((r) => r.id === id) || RANGES[1];

const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export const Mock = {
  reset() {
    const { txns, opening, next } = seed();
    db = { txns, opening, next, budgets: DEFAULT_BUDGETS, goals: DEFAULT_GOALS };
    saveDb(db);
  },

  summary(): FinancialSummary {
    const balance = db.opening + db.txns.reduce((a, t) => a + net(t), 0);
    const income = sumWin(0, 30, 'income');
    const expenses = sumWin(0, 30, 'expense');
    const trend: number[] = [];

    for (let off = 29; off >= 0; off--) {
      trend.push(
        balance -
          db.txns
            .filter((t) => daysAgo(t.date) < off)
            .reduce((a, t) => a + net(t), 0),
      );
    }

    return {
      balance,
      income,
      expenses,
      savings: income - expenses,
      prevIncome: sumWin(30, 60, 'income'),
      prevExpenses: sumWin(30, 60, 'expense'),
      changePct: DEMO_CHANGE_PCT,
      trend,
    };
  },

  list(params: {
    q?: string;
    category?: string;
    type?: string;
    from?: string;
    to?: string;
    cursor?: string;
    limit?: number;
    minAmount?: number;
    maxAmount?: number;
  }) {
    const {
      q = '',
      category,
      type,
      from,
      to,
      cursor,
      limit = 15,
      minAmount,
      maxAmount,
    } = params;

    const qq = q.trim();

    const items = sorted().filter(
      (t) =>
        (!qq || t.name.includes(qq) || t.category.includes(qq)) &&
        (!category || t.category === category) &&
        (!type || t.type === type) &&
        (!from || t.date >= from) &&
        (!to || t.date <= to) &&
        (minAmount == null || t.amount >= minAmount) &&
        (maxAmount == null || t.amount <= maxAmount),
    );

    const start = Math.max(0, Number(cursor || 0) || 0);
    const lim = Math.max(1, Number(limit || 15) || 15);
    const page = items.slice(start, start + lim);

    return {
      items: page,
      nextCursor: start + lim < items.length ? String(start + lim) : null,
      total: items.length,
    };
  },

  create(b: Partial<Transaction>): Transaction {
    const amount = Math.round(Number(b.amount) || 0);

    const t: Transaction = {
      id: 't' + db.next++,
      date: b.date || iso(today0()),
      name: (b.name || '').trim() || b.category || '',
      category: b.category || '',
      amount: Math.max(0, amount),
      type: b.type || 'expense',
      status: 'completed',
      source: b.source || 'web',
    };

    db.txns.push(t);
    saveDb(db);
    return t;
  },

  remove(id: string) {
    db.txns = db.txns.filter((t) => t.id !== id);
    saveDb(db);
  },

  series(rid: string): SeriesPoint[] {
    const r = rangeOf(rid);
    const size = r.days / r.n;
    const T = today0();

    const bs = Array.from({ length: r.n }, (_, i) => {
      const endOff = Math.floor((r.n - 1 - i) * size);
      const startOff = Math.ceil((r.n - i) * size) - 1;
      const e = addDays(T, -endOff);
      const s = addDays(T, -startOff);
      const label =
        r.n === r.days
          ? F.wd.format(e)
          : size >= 15
            ? F.mon.format(e)
            : F.dm.format(s);

      return {
        i,
        label,
        rangeLabel:
          startOff === endOff
            ? F.dm.format(e)
            : F.dm.format(s) + ' – ' + F.dm.format(e),
        income: 0,
        expenses: 0,
        net: 0,
      };
    });

    db.txns.forEach((t) => {
      const o = daysAgo(t.date);

      if (o >= 0 && o < r.days) {
        const b = bs[r.n - 1 - Math.floor(o / size)];

        if (b) {
          b[t.type === 'income' ? 'income' : 'expenses'] += t.amount;
        }
      }
    });

    return bs.map((b) => ({ ...b, net: b.income - b.expenses }));
  },

  categories(rid: string): CategoryStat[] {
    const r = rangeOf(rid);
    const cur: Record<string, number> = {};
    const prev: Record<string, number> = {};

    db.txns.forEach((t) => {
      if (t.type !== 'expense') return;

      const o = daysAgo(t.date);

      if (o >= 0 && o < r.days) {
        cur[t.category] = (cur[t.category] || 0) + t.amount;
      } else if (o >= r.days && o < 2 * r.days) {
        prev[t.category] = (prev[t.category] || 0) + t.amount;
      }
    });

    const total = Object.values(cur).reduce((a, b) => a + b, 0) || 1;

    return Object.entries(cur)
      .map(([category, amount]) => ({
        category,
        amount,
        share: Math.round((amount / total) * 100),
        prev: prev[category] || 0,
      }))
      .sort((a, b) => b.amount - a.amount);
  },

  insights(rid: string): Insight[] {
    const r = rangeOf(rid);
    const inc = sumWin(0, r.days, 'income');
    const exp = sumWin(0, r.days, 'expense');
    const prevExp = sumWin(r.days, 2 * r.days, 'expense');
    const cats = this.categories(rid);
    const out: Insight[] = [];

    if (cats[0]) {
      out.push({
        id: 'top',
        text: `بیشترین هزینه در این دوره «${cats[0].category}» بوده: ${toman(cats[0].amount)} (${fa(cats[0].share)}٪ از کل هزینه‌ها).`,
        type: 'info',
      });
    }

    if (prevExp > 0) {
      const p = Math.round(((exp - prevExp) / prevExp) * 100);

      out.push({
        id: 'chg',
        text: `هزینه‌ها ${fa(Math.abs(p))}٪ ${p <= 0 ? 'کمتر' : 'بیشتر'} از دوره‌ی قبل است.`,
        type: p > 0 ? 'warning' : 'success',
      });
    }

    if (inc > 0) {
      const s = Math.round(((inc - exp) / inc) * 100);

      out.push({
        id: 'sav',
        text:
          s >= 0
            ? `${fa(s)}٪ از درآمدت را پس‌انداز کرده‌ای.`
            : `هزینه‌هایت ${toman(exp - inc)} از درآمدت بیشتر بوده.`,
        type: s >= 20 ? 'success' : s < 0 ? 'warning' : 'info',
      });
    }

    if (exp > 0) {
      const avg = exp / r.days;

      out.push({
        id: 'avg',
        text: `میانگین هزینه‌ی روزانه‌ات ${toman(avg)} است. با همین روند، ۳۰ روز آینده حدود ${toman(avg * 30)} خرج می‌شود.`,
        type: 'info',
      });
    }

    return out;
  },

  prediction(rid: string) {
    const series = this.series(rid);
    const expValues = series.map((s) => s.expenses);
    const incValues = series.map((s) => s.income);
    const predicted = predictNext(expValues, 3);
    const predictedInc = predictNext(incValues, 3);
    const labels = ['ماه آینده', 'دو ماه دیگر', 'سه ماه دیگر'];

    return predicted.map((v, i) => ({
      label: labels[i],
      expenses: Math.round(v),
      income: Math.round(predictedInc[i]),
    }));
  },

  getBudgets(): BudgetItem[] {
    return db.budgets;
  },

  setBudgets(b: BudgetItem[]) {
    db.budgets = b;
    saveDb(db);
  },

  getGoals(): SavingsGoal[] {
    return db.goals;
  },

  setGoals(g: SavingsGoal[]) {
    db.goals = g;
    saveDb(db);
  },

  budgetStatus() {
    const budgets = db.budgets;
    const now = new Date();
    const monthStart = iso(new Date(now.getFullYear(), now.getMonth(), 1));

    return budgets.map((b) => {
      const spent = db.txns
        .filter(
          (t) =>
            t.type === 'expense' &&
            t.category === b.category &&
            t.date >= monthStart,
        )
        .reduce((a, t) => a + t.amount, 0);

      return {
        ...b,
        spent,
        pct: b.limit > 0 ? Math.round((spent / b.limit) * 100) : 0,
      };
    });
  },

  monthlyComparison() {
    const T = today0();

    return Array.from({ length: 6 }, (_, i) => {
      const mStart = new Date(T.getFullYear(), T.getMonth() - i, 1);
      const mEnd = new Date(T.getFullYear(), T.getMonth() - i + 1, 0);
      const label = F.ms.format(mStart);

      const income = db.txns
        .filter(
          (t) =>
            t.type === 'income' &&
            t.date >= iso(mStart) &&
            t.date <= iso(mEnd),
        )
        .reduce((a, t) => a + t.amount, 0);

      const expenses = db.txns
        .filter(
          (t) =>
            t.type === 'expense' &&
            t.date >= iso(mStart) &&
            t.date <= iso(mEnd),
        )
        .reduce((a, t) => a + t.amount, 0);

      return { label, income, expenses, net: income - expenses };
    }).reverse();
  },
};

export const api = {
  async summary() {
    await sleep(150);
    return Mock.summary();
  },

  async list(params: Parameters<typeof Mock.list>[0]) {
    await sleep(120);
    return Mock.list(params);
  },

  async create(b: Partial<Transaction>) {
    await sleep(180);
    return Mock.create(b);
  },

  async remove(id: string) {
    await sleep(120);
    return Mock.remove(id);
  },

  async series(rid: string) {
    await sleep(140);
    return Mock.series(rid);
  },

  async categories(rid: string) {
    await sleep(140);
    return Mock.categories(rid);
  },

  async insights(rid: string) {
    await sleep(140);
    return Mock.insights(rid);
  },

  async prediction(rid: string) {
    await sleep(140);
    return Mock.prediction(rid);
  },

  async monthlyComparison() {
    await sleep(140);
    return Mock.monthlyComparison();
  },

  async getBudgets() {
    await sleep(80);
    return Mock.getBudgets();
  },

  async setBudgets(b: BudgetItem[]) {
    await sleep(80);
    Mock.setBudgets(b);
  },

  async getGoals() {
    await sleep(80);
    return Mock.getGoals();
  },

  async setGoals(g: SavingsGoal[]) {
    await sleep(80);
    Mock.setGoals(g);
  },

  async budgetStatus() {
    await sleep(100);
    return Mock.budgetStatus();
  },

  reset() {
    Mock.reset();
  },
};
