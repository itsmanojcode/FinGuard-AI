from backend.config import AUTO_ACTION_LIMIT, APPROVAL_LIMIT


def evaluate_action(amount, action):

    amount = abs(float(amount))

    if amount == 0:
        return {
            "status": "NO_ACTION",
            "approval_required": False,
            "reason": "No financial action required.",
            "action": action
        }

    if amount <= AUTO_ACTION_LIMIT:
        return {
            "status": "ALLOWED",
            "approval_required": False,
            "reason": "Within configured autonomous-action limit.",
            "action": action
        }

    if amount <= APPROVAL_LIMIT:
        return {
            "status": "APPROVAL_REQUIRED",
            "approval_required": True,
            "reason": "Amount requires human approval.",
            "action": action
        }

    return {
        "status": "BLOCKED",
        "approval_required": True,
        "reason": "Amount exceeds configured approval limit.",
        "action": action
    }