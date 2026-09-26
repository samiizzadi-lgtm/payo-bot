import React, {
  createContext,
  useContext,
  useMemo,
  useState,
  useCallback,
  useEffect,
  useRef,
} from 'react';
import { Transaction, BudgetItem, SavingsGoal } from './data';
import { api } from './mock';

export interface Toast {
  id: number;
  title: string;
  detail?: string;
  kind?: 'success' | 'error' | 'info';
}

export type ModalState =
  | null
  | { kind: 'add'; type: 'income' | 'expense' }
  | { kind: 'tx'; t: Transaction }
  | { kind: 'budget' }
  | { kind: 'goal'; goal?: SavingsGoal };

interface StoreValue {
  version: number;
  toasts: Toast[];
  modal: ModalState;
  toast: (title: string, detail?: string, kind?: Toast['kind']) => void;
  openAdd: (type: 'income' | 'expense') => void;
  openTx: (t: Transaction) => void;
  openBudget: () => void;
  openGoal: (goal?: SavingsGoal) => void;
  closeModal: () => void;
  addTx: (b: Partial<Transaction>) => Promise<Transaction>;
  removeTx: (id: string) => Promise<void>;
  budgets: BudgetItem[];
  setBudgets: (b: BudgetItem[]) => Promise<void>;
  goals: SavingsGoal[];
  setGoals: (g: SavingsGoal[]) => Promise<void>;
  budgetAlerts: string[];
}

const Store = createContext<StoreValue | null>(null);

export const useStore = (): StoreValue => {
  const context = useContext(Store);

  if (!context) {
    throw new Error('useStore must be used inside StoreProvider');
  }

  return context;
};

export function StoreProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [version, setVersion] = useState(0);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [modal, setModal] = useState<ModalState>(null);
  const [budgets, setBudgetsState] = useState<BudgetItem[]>([]);
  const [goals, setGoalsState] = useState<SavingsGoal[]>([]);
  const [budgetAlerts, setBudgetAlerts] = useState<string[]>([]);

  const toastTimers = useRef<Map<number, ReturnType<typeof setTimeout>>>(
    new Map()
  );

  useEffect(() => {
    let active = true;

    const loadInitialData = async () => {
      try {
        const [loadedBudgets, loadedGoals] = await Promise.all([
          api.getBudgets(),
          api.getGoals(),
        ]);

        if (!active) return;

        setBudgetsState(loadedBudgets);
        setGoalsState(loadedGoals);
      } catch (error) {
        console.error('Initial store loading error:', error);
      }
    };

    void loadInitialData();

    return () => {
      active = false;

      toastTimers.current.forEach((timer) => clearTimeout(timer));
      toastTimers.current.clear();
    };
  }, []);

  useEffect(() => {
    if (budgets.length === 0) {
      setBudgetAlerts([]);
      return;
    }

    let active = true;

    const loadBudgetStatus = async () => {
      try {
        const statuses = await api.budgetStatus();

        if (!active) return;

        const alerts = statuses
          .filter((status) => Number(status.pct) >= 80)
          .map((status) =>
            Number(status.pct) >= 100
              ? `بودجه‌ی ${status.category} تموم شد!`
              : `${status.pct}٪ بودجه‌ی ${status.category} مصرف شد.`
          );

        setBudgetAlerts(alerts);
      } catch (error) {
        console.error('Budget status error:', error);
        if (active) setBudgetAlerts([]);
      }
    };

    void loadBudgetStatus();

    return () => {
      active = false;
    };
  }, [version, budgets]);

  const toast = useCallback(
    (
      title: string,
      detail?: string,
      kind: Toast['kind'] = 'success'
    ) => {
      const id = Date.now() + Math.random();

      setToasts((current) => [
        ...current,
        { id, title, detail, kind },
      ]);

      const timer = setTimeout(() => {
        setToasts((current) =>
          current.filter((item) => item.id !== id)
        );
        toastTimers.current.delete(id);
      }, 3600);

      toastTimers.current.set(id, timer);
    },
    []
  );

  const addTx = useCallback(
    async (data: Partial<Transaction>) => {
      const transaction = await api.create(data);
      setVersion((current) => current + 1);
      return transaction;
    },
    []
  );

  const removeTx = useCallback(async (id: string) => {
    await api.remove(id);
    setVersion((current) => current + 1);
  }, []);

  const setBudgets = useCallback(async (nextBudgets: BudgetItem[]) => {
    await api.setBudgets(nextBudgets);
    setBudgetsState(nextBudgets);
  }, []);

  const setGoals = useCallback(async (nextGoals: SavingsGoal[]) => {
    await api.setGoals(nextGoals);
    setGoalsState(nextGoals);
  }, []);

  const openAdd = useCallback((type: 'income' | 'expense') => {
    setModal({ kind: 'add', type });
  }, []);

  const openTx = useCallback((transaction: Transaction) => {
    setModal({ kind: 'tx', t: transaction });
  }, []);

  const openBudget = useCallback(() => {
    setModal({ kind: 'budget' });
  }, []);

  const openGoal = useCallback((goal?: SavingsGoal) => {
    setModal({ kind: 'goal', goal });
  }, []);

  const closeModal = useCallback(() => {
    setModal(null);
  }, []);

  const value = useMemo<StoreValue>(
    () => ({
      version,
      toasts,
      modal,
      toast,
      openAdd,
      openTx,
      openBudget,
      openGoal,
      closeModal,
      addTx,
      removeTx,
      budgets,
      setBudgets,
      goals,
      setGoals,
      budgetAlerts,
    }),
    [
      version,
      toasts,
      modal,
      toast,
      openAdd,
      openTx,
      openBudget,
      openGoal,
      closeModal,
      addTx,
      removeTx,
      budgets,
      setBudgets,
      goals,
      setGoals,
      budgetAlerts,
    ]
  );

  return <Store.Provider value={value}>{children}</Store.Provider>;
}
