const isValidDate = (date: Date) =>
  date instanceof Date && Number.isFinite(date.getTime());

const safeNumber = (value: number, fallback = 0) =>
  Number.isFinite(value) ? value : fallback;

export const toLatin = (s: string | number) =>
  String(s)
    .replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d)))
    .replace(/[٠-٩]/g, (d) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(d)));

export const fa = (n: number) =>
  Math.round(safeNumber(n)).toLocaleString('fa-IR');

export const toman = (n: number) => fa(n) + ' تومان';

export const short = (n: number) => {
  const value = safeNumber(n);
  const abs = Math.abs(value);

  if (abs >= 1e6) {
    return (
      (value / 1e6).toLocaleString('fa-IR', {
        maximumFractionDigits: 1,
      }) + ' م'
    );
  }

  if (abs >= 1e3) {
    return fa(value / 1e3) + ' ه';
  }

  return fa(value);
};

const pad = (n: number) => String(n).padStart(2, '0');

export const iso = (date: Date) => {
  if (!isValidDate(date)) return '';

  return (
    date.getFullYear() +
    '-' +
    pad(date.getMonth() + 1) +
    '-' +
    pad(date.getDate())
  );
};

export const parseISO = (value: string) => {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(
    toLatin(value).trim()
  );

  if (!match) return new Date(NaN);

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);

  const date = new Date(year, month - 1, day);

  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return new Date(NaN);
  }

  return date;
};

export const today0 = () => {
  const date = new Date();
  return new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate()
  );
};

export const addDays = (date: Date, amount: number) => {
  if (!isValidDate(date) || !Number.isFinite(amount)) {
    return new Date(NaN);
  }

  return new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate() + Math.trunc(amount)
  );
};

export const daysAgo = (value: string) => {
  const date = parseISO(value);

  if (!isValidDate(date)) return NaN;

  return Math.round(
    (today0().getTime() - date.getTime()) / 864e5
  );
};

const fmt = (options: Intl.DateTimeFormatOptions) =>
  new Intl.DateTimeFormat('fa-IR-u-ca-persian', options);

export const F = {
  dm: fmt({ day: 'numeric', month: 'long' }),
  full: fmt({
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }),
  wd: fmt({ weekday: 'short' }),
  mon: fmt({ month: 'long' }),
  ms: fmt({ month: 'short' }),
};

export const dateLabel = (value: string) => {
  const elapsed = daysAgo(value);

  if (!Number.isFinite(elapsed)) return 'تاریخ نامعتبر';
  if (elapsed === 0) return 'امروز';
  if (elapsed === 1) return 'دیروز';

  return F.dm.format(parseISO(value));
};

export const fullDate = (value: string) => {
  const date = parseISO(value);

  return isValidDate(date) ? F.full.format(date) : 'تاریخ نامعتبر';
};

export const pctText = (
  cur: number,
  prev: number,
  more = 'بیشتر',
  less = 'کمتر'
) => {
  const current = safeNumber(cur);
  const previous = safeNumber(prev);

  if (!previous) return 'بدون داده‌ی دوره‌ی قبل';

  const percent = Math.round(
    ((current - previous) / Math.abs(previous)) * 100
  );

  return `${fa(Math.abs(percent))}٪ ${
    percent >= 0 ? more : less
  } از ماه قبل`;
};

export const linearRegression = (ys: number[]) => {
  const values = ys.map((value) => safeNumber(value));
  const count = values.length;

  if (count < 2) {
    return {
      slope: 0,
      intercept: values[0] || 0,
    };
  }

  const xs = values.map((_, index) => index);
  const meanX =
    xs.reduce((sum, value) => sum + value, 0) / count;
  const meanY =
    values.reduce((sum, value) => sum + value, 0) / count;

  const numerator = xs.reduce(
    (sum, x, index) =>
      sum + (x - meanX) * (values[index] - meanY),
    0
  );

  const denominator = xs.reduce(
    (sum, x) => sum + (x - meanX) ** 2,
    0
  );

  const slope =
    denominator === 0 ? 0 : numerator / denominator;
  const intercept = meanY - slope * meanX;

  return {
    slope: safeNumber(slope),
    intercept: safeNumber(intercept),
  };
};

export const predictNext = (ys: number[], steps = 3) => {
  const count = Number.isFinite(steps)
    ? Math.max(0, Math.min(120, Math.trunc(steps)))
    : 0;

  const { slope, intercept } = linearRegression(ys);
  const length = ys.length;

  return Array.from({ length: count }, (_, index) =>
    Math.max(
      0,
      safeNumber(slope * (length + index) + intercept)
    )
  );
};
