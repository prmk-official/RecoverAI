# This file contains the decision-making logic
# for recovering failed payments.


def decide_recovery_action(payment):
    """
    Decide the safest recovery action for a failed payment.

    The function receives one payment record and
    returns the action our system recommends.
    """

    # Get the important information from the payment.
    failure = payment["failure_reason"]
    retries = payment["retry_count"]
    successes = payment["previous_successes"]

    # Customers with a good payment history may be
    # worth retrying when they have not hit the retry limit.
    if failure == "insufficient_funds" and retries < 2 and successes >= 5:
        return "RETRY"

    # An expired card requires the customer to
    # provide a different payment method.
    elif failure == "expired_card":
        return "REQUEST_NEW_PAYMENT_METHOD"

    # Stop repeated automatic attempts.
    elif retries >= 3:
        return "STOP_AND_ESCALATE"

    # Anything unclear should be reviewed instead
    # of allowing the system to make a risky decision.
    else:
        return "REVIEW"

def validate_ai_decision(payment, ai_action, ai_confidence=1.0):
    """
    Validate an AI recommendation before execution.

    Python has final authority over whether an action
    is allowed.
    """

    # These are the only actions our system supports.
    allowed_actions = {
        "RETRY",
        "REQUEST_NEW_PAYMENT_METHOD",
        "STOP_AND_ESCALATE",
        "REVIEW",
    }

    # Never allow an unknown action.
    if ai_action not in allowed_actions:
        return "STOP_AND_ESCALATE"

    # Low-confidence AI decisions are sent for review.
    if ai_confidence < 0.70:
        return "REVIEW"

    # Never retry a payment that has already reached
    # the retry limit.
    if ai_action == "RETRY" and payment["retry_count"] >= 3:
        return "STOP_AND_ESCALATE"

    # An expired card cannot be fixed by retrying it.
    if (
        ai_action == "RETRY"
        and payment["failure_reason"] == "expired_card"
    ):
        return "REQUEST_NEW_PAYMENT_METHOD"

    # If all safety checks pass, approve the action.
    return ai_action