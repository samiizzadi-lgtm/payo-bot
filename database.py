import sqlite3
from pathlib import Path


DATABASE_FILE = Path(__file__).parent / "payo.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_amount INTEGER NOT NULL,
            current_amount INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    connection.commit()
    connection.close()


def add_transaction(user_id, transaction_type, category, amount):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO transactions
            (user_id, type, category, amount)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, transaction_type, category, amount),
        )
        connection.commit()
    finally:
        connection.close()


def get_transactions(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, type, category, amount
            FROM transactions
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_all_transactions():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, type, category, amount
            FROM transactions
            ORDER BY id ASC
            """
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_transaction(user_id, transaction_id):
    """
    دریافت یک تراکنش متعلق به همان کاربر
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, type, category, amount
            FROM transactions
            WHERE id = ? AND user_id = ?
            """,
            (transaction_id, user_id),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def update_transaction(user_id, transaction_id, new_amount):
    """
    ویرایش مبلغ تراکنش متعلق به همان کاربر.
    در صورت موفقیت True و در غیر این صورت False برمی‌گرداند.
    """
    if not isinstance(new_amount, int) or new_amount <= 0:
        return False

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE transactions
            SET amount = ?
            WHERE id = ? AND user_id = ?
            """,
            (new_amount, transaction_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_financial_summary(user_id):
    transactions = get_transactions(user_id)

    total_income = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "income"
    )

    total_expense = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "expense"
    )

    balance = total_income - total_expense

    return {
        "income": total_income,
        "expense": total_expense,
        "balance": balance,
        "transaction_count": len(transactions),
    }


def add_goal(user_id, name, target_amount):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO goals
            (user_id, name, target_amount, current_amount)
            VALUES (?, ?, ?, 0)
            """,
            (user_id, name, target_amount),
        )
        connection.commit()
    finally:
        connection.close()


def get_user_goals(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, name, target_amount, current_amount
            FROM goals
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def deposit_to_goal(user_id, goal_id, amount):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE goals
            SET current_amount = current_amount + ?
            WHERE id = ? AND user_id = ?
            """,
            (amount, goal_id, user_id),
        )
        connection.commit()
    finally:
        connection.close()


def withdraw_from_goal(user_id, goal_id, amount):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE goals
            SET current_amount = MAX(0, current_amount - ?)
            WHERE id = ? AND user_id = ?
            """,
            (amount, goal_id, user_id),
        )
        connection.commit()
    finally:
        connection.close()


init_database()