import pandas as pd

from src.razorpay.recovery_engine import decide_recovery_action
from src.razorpay.simulator import execute_action


def run_baseline(payments):
    """
    Run the original rule-based recovery system.

    This is our official Python-only baseline.
    """

    results = []

    for _, payment in payments.iterrows():

        # Convert the Pandas row into a normal dictionary.
        payment = payment.to_dict()

        # Let the original Python rules choose the action.
        action = decide_recovery_action(payment)

        # Execute the selected action in our simulator.
        result = execute_action(payment, action)

        # Money is recovered only when the simulator
        # reports a successful recovery.
        recovered_amount = (
            payment["amount"] if result == "RECOVERED" else 0
        )

        # Save the complete result for this payment.
        results.append({
            "transaction_id": payment["transaction_id"],
            "amount": payment["amount"],
            "failure_reason": payment["failure_reason"],
            "retry_count": payment["retry_count"],
            "action": action,
            "result": result,
            "recovered_amount": recovered_amount,
        })

    # Convert all payment results into a DataFrame.
    return pd.DataFrame(results)


def run_ai_informed_policy(payments):
    """
    Run the AI-informed recovery policy across all payments.

    The rules below were based on the contextual patterns
    we observed during our Gemini experiment.

    Gemini is NOT called here. This allows us to evaluate
    the policy across all 500 payments without exceeding
    the API quota.
    """

    results = []

    for _, payment in payments.iterrows():

        # Convert the Pandas row into a normal dictionary.
        payment = payment.to_dict()

        failure = payment["failure_reason"]
        retries = payment["retry_count"]
        successes = payment["previous_successes"]

        # ---------------------------------------------------------
        # Rule 1: Expired cards need a new payment method.
        # ---------------------------------------------------------
        if failure == "expired_card":

            action = "REQUEST_NEW_PAYMENT_METHOD"
            reason = "Card is expired."

        # ---------------------------------------------------------
        # Rule 2: Never keep retrying indefinitely.
        # ---------------------------------------------------------
        elif retries >= 3:

            action = "STOP_AND_ESCALATE"
            reason = "Maximum retry limit reached."

        # ---------------------------------------------------------
        # Rule 3: A bank error with no previous retry
        # may be temporary.
        # ---------------------------------------------------------
        elif failure == "bank_error" and retries == 0:

            action = "RETRY"
            reason = "Bank error with no previous retry."

        # ---------------------------------------------------------
        # Rule 4: A timeout is uncertain, so send it
        # for manual review.
        # ---------------------------------------------------------
        elif failure == "timeout":

            action = "REVIEW"
            reason = "Timeout requires further investigation."

        # ---------------------------------------------------------
        # Rule 5: Strong payment history + insufficient funds
        # + few retries → retry.
        # ---------------------------------------------------------
        elif (
            failure == "insufficient_funds"
            and successes >= 3
            and retries <= 1
        ):

            action = "RETRY"
            reason = (
                "Customer has a strong payment history "
                "and has not exceeded the retry limit."
            )

        # ---------------------------------------------------------
        # Rule 6: Insufficient funds with weak history or
        # repeated retries → request another payment method.
        # ---------------------------------------------------------
        elif failure == "insufficient_funds":

            action = "REQUEST_NEW_PAYMENT_METHOD"
            reason = (
                "Insufficient funds with weak payment history "
                "or repeated failures."
            )

        # ---------------------------------------------------------
        # Rule 7: Unexpected cases go to manual review.
        # ---------------------------------------------------------
        else:

            action = "REVIEW"
            reason = "No specific recovery policy matched."

        # Execute the selected action in the simulator.
        result = execute_action(payment, action)

        # Count the payment amount as recovered only when
        # the simulator reports a successful recovery.
        recovered_amount = (
            payment["amount"] if result == "RECOVERED" else 0
        )

        # Save the decision and outcome.
        results.append({
            "transaction_id": payment["transaction_id"],
            "amount": payment["amount"],
            "failure_reason": failure,
            "retry_count": retries,
            "previous_successes": successes,
            "action": action,
            "reason": reason,
            "result": result,
            "recovered_amount": recovered_amount,
        })

    # Return all 500 results as a DataFrame.
    return pd.DataFrame(results)