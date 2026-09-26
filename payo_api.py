from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
import sqlite3

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "payo.db"

app = FastAPI(title="Payo Local API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def con() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def ensure_schema() -> None:
    with con() as db:
        cols = {r["name"] for r in db.execute("PRAGMA table_info(transactions)")}
        if not cols:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount INTEGER NOT NULL
                )
                """
            )
            cols = {r["name"] for r in db.execute("PRAGMA table_info(transactions)")}

        if "created_at" not in cols:
            db.execute("ALTER TABLE transactions ADD COLUMN created_at TEXT")
        if "name" not in cols:
            db.execute("ALTER TABLE transactions ADD COLUMN name TEXT")

        db.execute("UPDATE transactions SET name = category WHERE name IS NULL OR name = ''")
        db.execute(
            "UPDATE transactions SET created_at = date('now','localtime') "
            "WHERE created_at IS NULL OR created_at = ''"
        )

        db.execute(
            """
            CREATE TRIGGER IF NOT EXISTS payo_tx_defaults
            AFTER INSERT ON transactions
            BEGIN
              UPDATE transactions
                 SET name = CASE WHEN NEW.name IS NULL OR NEW.name = '' THEN NEW.category ELSE NEW.name END,
                     created_at = CASE WHEN NEW.created_at IS NULL OR NEW.created_at = ''
                                      THEN date('now','localtime') ELSE NEW.created_at END
               WHERE id = NEW.id;
            END;
            """
        )

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS web_budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                limit_amount INTEGER NOT NULL DEFAULT 0,
                UNIQUE(user_id, category)
            )
            """
        )

        db.commit()


ensure_schema()


# Local-development identity only.
# In production this should be replaced with verified Telegram WebApp initData.
def user_id_from_header(x_dev_user_id: str = Header("")) -> int:
    try:
        uid = int(x_dev_user_id)
    except (TypeError, ValueError):
        raise HTTPException(401, "X-Dev-User-Id is required for local dashboard testing")
    if uid <= 0:
        raise HTTPException(401, "invalid user id")
    return uid


class NewTx(BaseModel):
    type: str
    amount: int = Field(gt=0)
    category: str
    name: str = ""
    date: str = ""


class BudgetItem(BaseModel):
    category: str
    limit: int = Field(ge=0)


class GoalItem(BaseModel):
    id: str | None = None
    name: str
    target: int = Field(ge=0)
    current: int = Field(ge=0)
    deadline: str | None = None
    color: str = "#2f6bff"


INCOME_TYPES = {"income", "درآمد"}
EXPENSE_TYPES = {"expense", "هزینه"}


def tx_dict(row: sqlite3.Row) -> dict[str, Any]:
    raw_type = str(row["type"])
    tx_type = "income" if raw_type in INCOME_TYPES else "expense"
    return {
        "id": str(row["id"]),
        "date": str(row["created_at"] or date.today().isoformat())[:10],
        "name": row["name"] or row["category"],
        "category": row["category"],
        "amount": int(row["amount"]),
        "type": tx_type,
        "status": "completed",
        "source": "telegram",
    }


def parse_iso(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None


def all_user_transactions(uid: int) -> list[dict[str, Any]]:
    with con() as db:
        rows = db.execute(
            "SELECT id, type, category, amount, name, created_at "
            "FROM transactions WHERE user_id = ? ORDER BY created_at DESC, id DESC",
            (uid,),
        ).fetchall()
    return [tx_dict(r) for r in rows]


def filtered_transactions(uid: int, category: str | None, tx_type: str | None,
                          q: str | None, start: str | None, end: str | None,
                          min_amount: int | None, max_amount: int | None) -> list[dict[str, Any]]:
    rows = all_user_transactions(uid)
    qn = (q or "").strip().lower()
    out = []
    for t in rows:
        if category and t["category"] != category:
            continue
        if tx_type and t["type"] != tx_type:
            continue
        if qn and qn not in t["name"].lower() and qn not in t["category"].lower():
            continue
        if start and t["date"] < start:
            continue
        if end and t["date"] > end:
            continue
        if min_amount is not None and t["amount"] < min_amount:
            continue
        if max_amount is not None and t["amount"] > max_amount:
            continue
        out.append(t)
    return out


def range_days(rid: str) -> tuple[int, int]:
    mapping = {"7d": (7, 7), "30d": (30, 10), "3m": (90, 13), "6m": (180, 12), "1y": (365, 12)}
    return mapping.get(rid, mapping["30d"])


def series_for(uid: int, rid: str) -> list[dict[str, Any]]:
    days, points = range_days(rid)
    today = date.today()
    bins: list[dict[str, Any]] = []
    for i in range(points):
        start_off = int((points - i - 1) * days / points)
        end_off = int(((points - i) * days / points)) - 1
        d_end = today - timedelta(days=max(end_off, 0))
        d_start = today - timedelta(days=max(start_off, 0))
        if d_start > d_end:
            d_start = d_end
        label = d_end.strftime("%m/%d")
        bins.append({
            "label": label,
            "rangeLabel": f"{d_start.strftime('%Y-%m-%d')} – {d_end.strftime('%Y-%m-%d')}",
            "income": 0,
            "expenses": 0,
            "net": 0,
            "_start": d_start,
            "_end": d_end,
        })

    for t in all_user_transactions(uid):
        td = parse_iso(t["date"])
        if td is None:
            continue
        for b in bins:
            if b["_start"] <= td <= b["_end"]:
                if t["type"] == "income":
                    b["income"] += t["amount"]
                else:
                    b["expenses"] += t["amount"]
                break

    for b in bins:
        b["net"] = b["income"] - b["expenses"]
        b.pop("_start", None)
        b.pop("_end", None)
    return bins


def categories_for(uid: int, rid: str) -> list[dict[str, Any]]:
    days, _ = range_days(rid)
    today = date.today()
    cur_start = today - timedelta(days=days - 1)
    prev_start = cur_start - timedelta(days=days)
    totals: dict[str, int] = {}
    prev: dict[str, int] = {}
    for t in all_user_transactions(uid):
        if t["type"] != "expense":
            continue
        td = parse_iso(t["date"])
        if not td:
            continue
        if cur_start <= td <= today:
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
        elif prev_start <= td < cur_start:
            prev[t["category"]] = prev.get(t["category"], 0) + t["amount"]
    total = sum(totals.values()) or 1
    return [
        {"category": cat, "amount": amount, "share": round(amount * 100 / total), "prev": prev.get(cat, 0)}
        for cat, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True)
    ]


def summary_for(uid: int) -> dict[str, Any]:
    txs = all_user_transactions(uid)
    total_income = sum(t["amount"] for t in txs if t["type"] == "income")
    total_expense = sum(t["amount"] for t in txs if t["type"] == "expense")
    today = date.today()
    cur_start = today - timedelta(days=29)
    prev_start = today - timedelta(days=59)
    cur_income = cur_expense = prev_income = prev_expense = 0
    for t in txs:
        td = parse_iso(t["date"])
        if not td:
            continue
        if cur_start <= td <= today:
            if t["type"] == "income": cur_income += t["amount"]
            else: cur_expense += t["amount"]
        elif prev_start <= td < cur_start:
            if t["type"] == "income": prev_income += t["amount"]
            else: prev_expense += t["amount"]

    # Cumulative movement for the latest 30 days, starting from zero.
    trend = []
    running = 0
    for off in range(29, -1, -1):
        d = today - timedelta(days=off)
        delta = sum(
            (t["amount"] if t["type"] == "income" else -t["amount"])
            for t in txs if t["date"] == d.isoformat()
        )
        running += delta
        trend.append(running)

    change_pct = round(((cur_expense - prev_expense) / prev_expense) * 100, 1) if prev_expense else 0
    return {
        "balance": total_income - total_expense,
        "income": cur_income,
        "expenses": cur_expense,
        "savings": cur_income - cur_expense,
        "prevIncome": prev_income,
        "prevExpenses": prev_expense,
        "changePct": change_pct,
        "trend": trend,
    }


def budgets_for(uid: int) -> list[dict[str, Any]]:
    with con() as db:
        rows = db.execute(
            "SELECT category, limit_amount FROM web_budgets WHERE user_id = ? ORDER BY id",
            (uid,),
        ).fetchall()
    return [{"category": r["category"], "limit": int(r["limit_amount"])} for r in rows]


def budget_status_for(uid: int) -> list[dict[str, Any]]:
    budgets = budgets_for(uid)
    today = date.today()
    month_start = date(today.year, today.month, 1)
    txs = all_user_transactions(uid)
    out = []
    for b in budgets:
        spent = sum(
            t["amount"] for t in txs
            if t["type"] == "expense" and t["category"] == b["category"]
            and (parse_iso(t["date"]) or today) >= month_start
        )
        pct = round(spent * 100 / b["limit"]) if b["limit"] > 0 else 0
        out.append({**b, "spent": spent, "pct": pct})
    return out


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "db": str(DB_PATH.name)}


@app.get("/me")
def me(x_dev_user_id: str = Header("")):
    return {"id": user_id_from_header(x_dev_user_id)}


@app.get("/transactions")
def transactions(
    x_dev_user_id: str = Header(""),
    q: str = "",
    category: str = "",
    type: str = "",
    from_: str = Query("", alias="from"),
    to: str = "",
    minAmount: int | None = None,
    maxAmount: int | None = None,
    limit: int = 15,
    cursor: int = 0,
):
    uid = user_id_from_header(x_dev_user_id)
    rows = filtered_transactions(uid, category or None, type or None, q, from_ or None, to or None, minAmount, maxAmount)
    limit = max(1, min(limit, 100))
    page = rows[cursor:cursor + limit]
    next_cursor = cursor + limit if cursor + limit < len(rows) else None
    return {"items": page, "nextCursor": str(next_cursor) if next_cursor is not None else None, "total": len(rows)}


@app.post("/transactions")
def create_transaction(t: NewTx, x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    if t.type not in {"income", "expense"}:
        raise HTTPException(422, "invalid type")
    created = t.date or date.today().isoformat()
    with con() as db:
        cur = db.execute(
            "INSERT INTO transactions (user_id, type, category, amount, name, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (uid, t.type, t.category, t.amount, t.name or t.category, created),
        )
        row = db.execute(
            "SELECT id, type, category, amount, name, created_at FROM transactions WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()
    return tx_dict(row)


@app.delete("/transactions/{tx_id}", status_code=204)
def delete_transaction(tx_id: int, x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    with con() as db:
        db.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (tx_id, uid))


@app.get("/summary")
def get_summary(x_dev_user_id: str = Header("")):
    return summary_for(user_id_from_header(x_dev_user_id))


@app.get("/series/{rid}")
def get_series(rid: str, x_dev_user_id: str = Header("")):
    return series_for(user_id_from_header(x_dev_user_id), rid)


@app.get("/categories/{rid}")
def get_categories(rid: str, x_dev_user_id: str = Header("")):
    return categories_for(user_id_from_header(x_dev_user_id), rid)


@app.get("/insights/{rid}")
def get_insights(rid: str, x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    s = summary_for(uid)
    cats = categories_for(uid, rid)
    out = []
    if cats:
        out.append({"id": "top", "text": f"بیشترین هزینه در این دوره «{cats[0]['category']}» بوده: {cats[0]['amount']:,} تومان ({cats[0]['share']}٪).", "type": "info"})
    if s["prevExpenses"] > 0:
        p = round(((s["expenses"] - s["prevExpenses"]) / s["prevExpenses"]) * 100)
        out.append({"id": "chg", "text": f"هزینه‌های ۳۰ روز اخیر {abs(p)}٪ {'بیشتر' if p > 0 else 'کمتر'} از دوره‌ی قبل است.", "type": "warning" if p > 0 else "success"})
    if s["income"] > 0:
        rate = round((s["income"] - s["expenses"]) * 100 / s["income"])
        out.append({"id": "sav", "text": f"نرخ پس‌انداز این دوره {rate}٪ است.", "type": "success" if rate >= 20 else "info"})
    return out


@app.get("/prediction/{rid}")
def get_prediction(rid: str, x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    series = series_for(uid, rid)
    exp = [x["expenses"] for x in series]
    inc = [x["income"] for x in series]
    avg_exp = sum(exp[-3:]) / max(1, len(exp[-3:]))
    avg_inc = sum(inc[-3:]) / max(1, len(inc[-3:]))
    labels = ["ماه آینده", "دو ماه دیگر", "سه ماه دیگر"]
    return [{"label": labels[i], "expenses": round(avg_exp), "income": round(avg_inc)} for i in range(3)]


@app.get("/monthly-comparison")
def monthly_comparison(x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    txs = all_user_transactions(uid)
    today = date.today()
    out = []
    for offset in range(5, -1, -1):
        first = date(today.year, today.month, 1)
        y = first.year + (first.month - 1 - offset) // 12
        m = (first.month - 1 - offset) % 12 + 1
        start = date(y, m, 1)
        next_month = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
        end = next_month - timedelta(days=1)
        income = expense = 0
        for t in txs:
            td = parse_iso(t["date"])
            if td and start <= td <= end:
                if t["type"] == "income": income += t["amount"]
                else: expense += t["amount"]
        out.append({"label": f"{m:02d}/{y}", "income": income, "expenses": expense, "net": income - expense})
    return out


@app.get("/budgets")
def get_budgets(x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    current = budgets_for(uid)
    if current:
        return current
    defaults = [
        {"category": "غذا", "limit": 3000000},
        {"category": "حمل‌ونقل", "limit": 1000000},
        {"category": "خرید", "limit": 2000000},
        {"category": "قبوض", "limit": 1500000},
    ]
    with con() as db:
        db.executemany(
            "INSERT OR IGNORE INTO web_budgets (user_id, category, limit_amount) VALUES (?, ?, ?)",
            [(uid, x["category"], x["limit"]) for x in defaults],
        )
    return defaults


@app.post("/budgets")
def set_budgets(items: list[BudgetItem], x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    with con() as db:
        db.execute("DELETE FROM web_budgets WHERE user_id = ?", (uid,))
        db.executemany(
            "INSERT INTO web_budgets (user_id, category, limit_amount) VALUES (?, ?, ?)",
            [(uid, x.category, x.limit) for x in items],
        )
    return [x.model_dump() for x in items]


@app.get("/budget-status")
def get_budget_status(x_dev_user_id: str = Header("")):
    return budget_status_for(user_id_from_header(x_dev_user_id))


@app.get("/goals")
def get_goals(x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    with con() as db:
        rows = db.execute(
            "SELECT id, name, target_amount, current_amount FROM goals WHERE user_id = ? ORDER BY id",
            (uid,),
        ).fetchall()
    return [
        {"id": str(r["id"]), "name": r["name"], "target": int(r["target_amount"]), "current": int(r["current_amount"]), "deadline": None, "color": "#2f6bff"}
        for r in rows
    ]


@app.post("/goals")
def set_goals(items: list[GoalItem], x_dev_user_id: str = Header("")):
    uid = user_id_from_header(x_dev_user_id)
    with con() as db:
        db.execute("DELETE FROM goals WHERE user_id = ?", (uid,))
        for g in items:
            db.execute(
                "INSERT INTO goals (user_id, name, target_amount, current_amount) VALUES (?, ?, ?, ?)",
                (uid, g.name, g.target, g.current),
            )
    return [x.model_dump() for x in items]
