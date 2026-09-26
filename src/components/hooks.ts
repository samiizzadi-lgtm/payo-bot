import type { DependencyList } from 'react';
import { useEffect, useRef, useState } from 'react';
import { toLatin } from '../utils';

type ApiState<T> = {
  data: T | null;
  status: 'loading' | 'ready' | 'error';
  error: unknown;
};

export function useApi<T>(loader: () => Promise<T>, deps: DependencyList = []): ApiState<T> {
  const [state, setState] = useState<ApiState<T>>({ data: null, status: 'loading', error: null });
  useEffect(() => {
    let active = true;
    setState((s) => ({ ...s, status: 'loading', error: null }));
    Promise.resolve(loader()).then(
      (data) => active && setState({ data, status: 'ready', error: null }),
      (error) => active && setState({ data: null, status: 'error', error }),
    );
    return () => { active = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return state;
}

export function useDebounced<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = window.setTimeout(() => setDebounced(value), delay);
    return () => window.clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

export function useCountUp(target: number, duration = 650): number {
  const [value, setValue] = useState(target);
  const previous = useRef(target);
  useEffect(() => {
    const from = previous.current;
    const to = Number.isFinite(target) ? target : 0;
    previous.current = to;
    const start = performance.now();
    let frame = 0;
    const tick = (now: number) => {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setValue(from + (to - from) * eased);
      if (p < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [target, duration]);
  return value;
}

export function go(path: string): void {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  window.location.hash = normalized === '/' ? '/' : normalized;
}

export function useRoute() {
  const read = () => {
    const raw = window.location.hash.replace(/^#/, '') || '/';
    const [pathPart, queryString = ''] = raw.split('?');
    const path = pathPart || '/';
    return { path, query: new URLSearchParams(queryString) };
  };
  const [route, setRoute] = useState(read);
  useEffect(() => {
    const onHash = () => setRoute(read());
    window.addEventListener('hashchange', onHash);
    if (!window.location.hash) window.history.replaceState(null, '', '#/');
    return () => window.removeEventListener('hashchange', onHash);
  }, []);
  return route;
}
