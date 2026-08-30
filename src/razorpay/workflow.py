from src.razorpay.agent import (
    get_recovery_decision,
)

from src.razorpay.recovery_engine import (
    validate_ai_decision,
)

from src.razorpay.simulator import (
    execute_action,
)


def process_payment(payment):
    """
    Run one payment through the complete RecoverAI workflow.

    Flow:
    Payment
        ↓
    Decision (Python or Gemini)
        ↓
    Safety Check
        ↓
    Approved Action
        ↓
    Simulator
        ↓
    Result
    """

    # ---------------------------------------------------------
    # Step 1: Get a recovery decision.
    #
    # Python handles straightforward cases.
    # Gemini is used when additional reasoning is required.
    # ---------------------------------------------------------
    decision = get_recovery_decision(payment)

    # ---------------------------------------------------------
    # Step 2: Validate the proposed action.
    #
    # Python remains the final safety authority.
    # This prevents an unsafe AI recommendation from
    # being executed automatically.
    # ---------------------------------------------------------
    approved_action = validate_ai_decision(
        payment,
        decision.action,
        decision.confidence,
    )

    # ---------------------------------------------------------
    # Step 3: Execute ONLY the approved action.
    #
    # This uses our simulator instead of a real payment gateway.
    # ---------------------------------------------------------
    result = execute_action(
        payment,
        approved_action,
    )

    # ---------------------------------------------------------
    # Step 4: Calculate recovered revenue.
    #
    # A payment contributes to recovered revenue only when
    # the simulator reports a successful recovery.
    # ---------------------------------------------------------
    if result == "RECOVERED":
        recovered_amount = payment["amount"]
    else:
        recovered_amount = 0

    # ---------------------------------------------------------
    # Step 5: Return the complete decision and outcome.
    #
    # These fields can later be used for:
    # - evaluation
    # - audit logs
    # - dashboard
    # ---------------------------------------------------------
    return {
    "transaction_id": payment["transaction_id"],
    "amount": payment["amount"],
    "failure_reason": payment["failure_reason"],
    "decision_action": decision.action,
    "approved_action": approved_action,
    "confidence": decision.confidence,
    "reason": decision.reason,
    "result": result,
    "recovered_amount": recovered_amount,
}