from datetime import datetime


transactions = []
goals = []


def add_transaction(
    user_id: int,
    transaction_type: str,
    category: str,
    amount: float,
    description: str = "",
):
    transaction = {
        "user_id": user_id,
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description,
        "date": datetime.now(),
    }

    transactions.append(transaction)

    return transaction


def add_goal(
    user_id: int,
    name: str,
    target_amount: float,
):
    goal = {
        "id": len(goals) + 1,
        "user_id": user_id,
        "name": name,
        "target_amount": target_amount,
        "current_amount": 0,
        "created_at": datetime.now(),
    }

    goals.append(goal)

    return goal


def get_user_goals(user_id: int):
    return [
        goal
        for goal in goals
        if goal["user_id"] == user_id
    ]


def deposit_to_goal(
    user_id: int,
    goal_id: int,
    amount: float,
):
    for goal in goals:
        if goal["id"] == goal_id and goal["user_id"] == user_id:
            goal["current_amount"] += amount
            return goal

    return None


def withdraw_from_goal(
    user_id: int,
    goal_id: int,
    amount: float,
):
    for goal in goals:
        if goal["id"] == goal_id and goal["user_id"] == user_id:

            if amount > goal["current_amount"]:
                return None

            goal["current_amount"] -= amount

            return goal

    return None