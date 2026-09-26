import React from 'react';
import { ResponsiveContainer, AreaChart, Area, Tooltip } from 'recharts';

type SparklineProps = {
  data: number[];
};

export function Sparkline({ data }: SparklineProps) {
  const values = data.filter(Number.isFinite);
  if (values.length === 0) return <div style={{ height: 84 }} aria-hidden="true" />;

  const chartData = values.map((value, index) => ({ index, value }));

  return (
    <div style={{ width: '100%', height: 84 }} aria-hidden="true">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 8, right: 2, left: 2, bottom: 0 }}>
          <defs>
            <linearGradient id="payoSparkFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#2f6bff" stopOpacity={0.28} />
              <stop offset="100%" stopColor="#2f6bff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <Tooltip cursor={false} content={() => null} />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#2f6bff"
            strokeWidth={2.25}
            fill="url(#payoSparkFill)"
            isAnimationActive
            animationDuration={650}
            animationEasing="ease-in-out"
            dot={false}
            activeDot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
