import pandas as pd

from src.razorpay.agent import (
    ask_ai_for_decision,
    create_python_decision,
)

# Import the Python safety check.
from src.razorpay.recovery_engine import validate_ai_decision

# Import the payment simulator.
from src.razorpay.simulator import execute_action


def select_ai_sample(payments, sample_size=5):
    """
    Select a small group of ambiguous payments for AI testing.

    We keep the sample small because the Gemini free tier
    has a limited number of API requests.
    """

    # Select payment types where additional reasoning may help.
    candidates = payments[
        payments["failure_reason"].isin([
            "insufficient_funds",
            "bank_error",
            "timeout",
        ])
        & (payments["retry_count"] < 3)
    ]

    # Return only the requested number of payments.
    return candidates.head(sample_size)


def compare_decisions(payments):
    """
    Compare the Python baseline with Gemini on a small sample.

    This experiment compares recommendations only.
    It does NOT execute the payments.
    """

    # Select five ambiguous payments.
    sample = select_ai_sample(
        payments,
        sample_size=5,
    )

    results = []

    # Analyze each selected payment.
    for _, payment in sample.iterrows():

        # Convert the Pandas row into a normal Python dictionary.
        payment = payment.to_dict()

        # Ask the Python baseline for a decision.
        python_decision = create_python_decision(payment)

        # Ask Gemini for a decision.
        ai_decision = ask_ai_for_decision(payment)

        # If Python has no deterministic answer,
        # label it as AI_REQUIRED rather than calling it
        # a disagreement.
        python_action = (
            python_decision.action
            if python_decision
            else "AI_REQUIRED"
        )

        # True disagreement only happens when BOTH systems
        # actually provide an action and those actions differ.
        disagreement = (
            python_decision is not None
            and python_action != ai_decision.action
        )

                # ---------------------------------------------------------
        # Test what happens if we use the AI recommendation.
        # ---------------------------------------------------------

        approved_action = validate_ai_decision(
            payment,
            ai_decision.action,
            ai_decision.confidence,
        )

        # Simulate the approved action.
        ai_result = execute_action(
            payment,
            approved_action,
        )

        # Calculate how much money this AI decision recovered.
        if ai_result == "RECOVERED":
            ai_recovered_amount = payment["amount"]
        else:
            ai_recovered_amount = 0

        # Save the complete comparison.
        results.append({
            "transaction_id": payment["transaction_id"],
            "amount": payment["amount"],
            "failure_reason": payment["failure_reason"],
            "retry_count": payment["retry_count"],

            # Python baseline recommendation.
            "python_action": python_action,

            # Gemini recommendation.
            "ai_action": ai_decision.action,

            # AI confidence.
            "ai_confidence": ai_decision.confidence,

            # AI explanation.
            "ai_reason": ai_decision.reason,

            # Action allowed by our safety layer.
            "approved_action": approved_action,

            # What happened after the simulated action.
            "ai_result": ai_result,

            # Money recovered from this payment.
            "ai_recovered_amount": ai_recovered_amount,

            # True only when Python and AI both have
            # an action and those actions are different.
            "disagreement": disagreement,
        })

    # Convert the results into a table.
    return pd.DataFrame(results)

