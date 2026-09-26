import React, { useId } from 'react';

type SparklineProps = {
  data: number[];
};

export function Sparkline({ data }: SparklineProps) {
  const W = 300;
  const H = 84;
  const gradientId = `sparkfill-${useId().replace(/:/g, '')}`;

  const values = data.filter(Number.isFinite);

  if (values.length === 0) {
    return (
      <svg
        width="100%"
        height={H}
        viewBox={`0 0 ${W} ${H}`}
        aria-hidden="true"
        style={{ display: 'block' }}
      />
    );
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  const pts = values.map((value, index) => {
    const x =
      values.length === 1
        ? W / 2
        : (index / (values.length - 1)) * W;

    const y = H - 8 - ((value - min) / range) * (H - 20);

    return [x, y] as [number, number];
  });

  const d = pts
    .map((point, index) =>
      `${index === 0 ? 'M' : 'L'}${point[0].toFixed(1)} ${point[1].toFixed(1)}`
    )
    .join(' ');

  const fillPath =
    values.length === 1
      ? ''
      : `${d} L${W} ${H} L0 ${H} Z`;

  return (
    <svg
      width="100%"
      height={H}
      viewBox={`0 0 ${W} ${H}`}
      preserveAspectRatio="none"
      aria-hidden="true"
      style={{
        display: 'block',
        animation:
          'wipe 1.1s cubic-bezier(0.2, 0.7, 0.2, 1) 0.1s both',
      }}
    >
      <defs>
        <linearGradient
          id={gradientId}
          x1="0"
          x2="0"
          y1="0"
          y2="1"
        >
          <stop offset="0" stopColor="#2f6bff" stopOpacity="0.32" />
          <stop offset="1" stopColor="#2f6bff" stopOpacity="0" />
        </linearGradient>
      </defs>

      {fillPath && (
        <path d={fillPath} fill={`url(#${gradientId})`} />
      )}

      <path
        fill="none"
        stroke="#2f6bff"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
        d={d}
      />
    </svg>
  );
}
