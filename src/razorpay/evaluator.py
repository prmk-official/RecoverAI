import pandas as pd


def evaluate_results(results):
    """
    Calculate the performance of RecoverAI.

    This function only measures results.
    It does NOT make recovery decisions.
    """

    # Convert all payment results into a table.
    results_df = pd.DataFrame(results)

    # Calculate the total amount of money that was at risk.
    total_at_risk = results_df["amount"].sum()

    # Calculate the amount that was successfully recovered.
    total_recovered = results_df["recovered_amount"].sum()

    # Count how many payments were successfully recovered.
    payments_recovered = (
        results_df["result"] == "RECOVERED"
    ).sum()

    # Calculate the percentage of at-risk revenue recovered.
    recovery_rate = (
        total_recovered / total_at_risk
    ) * 100

    # Return all important metrics together.
    return {
        "total_payments": len(results_df),
        "total_at_risk": total_at_risk,
        "payments_recovered": payments_recovered,
        "total_recovered": total_recovered,
        "recovery_rate": recovery_rate,
    }