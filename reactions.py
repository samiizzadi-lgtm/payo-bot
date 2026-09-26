from telegram import ReactionTypeEmoji


async def react_to_message(message, emoji):
    try:
        result = await message.get_bot().set_message_reaction(
            chat_id=message.chat_id,
            message_id=message.message_id,
            reaction=[
                ReactionTypeEmoji(emoji=emoji)
            ],
            is_big=False,
        )

        print(
            f"Reaction sent: {emoji} | "
            f"message={message.message_id} | "
            f"result={result}"
        )

        return result

    except Exception as error:
        print(
            f"Reaction Error: {type(error).__name__}: {error}"
        )

        return False


def get_expense_reaction(amount):
    if amount >= 1_000_000:
        return "😱"

    if amount >= 500_000:
        return "💸"

    if amount >= 100_000:
        return "😬"

    return "👍"


def get_income_reaction(amount):
    if amount >= 5_000_000:
        return "🤑"

    if amount >= 1_000_000:
        return "💰"

    return "👍"


def get_radar_reaction(report):
    if "🔴" in report or "🚨" in report:
        return "😱"

    if "🟡" in report or "⚠️" in report:
        return "🤔"

    if "🟢" in report:
        return "🚀"

    return "👍"


def get_goal_reaction():
    return "🎯"