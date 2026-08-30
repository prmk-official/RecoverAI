import pandas as pd

from src.razorpay.workflow import process_payment
from src.razorpay.evaluator import evaluate_results
from src.razorpay.audit import save_audit_log


# Load the same 500 synthetic payments used by our baseline.
payments = pd.read_csv("data/payments.csv")


# Store the result of every payment.
results = []


print("\n========== FINAL HYBRID RECOVERAI EVALUATION ==========")


# Process all 500 payments through the actual RecoverAI workflow.
for _, payment in payments.iterrows():

    # Convert the Pandas row into a normal Python dictionary.
    payment = payment.to_dict()

    # Run:
    # Decision → Safety Check → Action → Result
    result = process_payment(payment)

    results.append(result)


# Convert all results into a DataFrame.
results = pd.DataFrame(results)


# Save the complete RecoverAI audit log.
save_audit_log(
    results,
    "data/recoverai_audit.csv",
)


# Calculate final performance metrics.
metrics = evaluate_results(results)


print("\n========== FINAL RESULTS ==========")

print("Total payments:", metrics["total_payments"])
print("Revenue at risk: ₹", metrics["total_at_risk"])
print("Payments recovered:", metrics["payments_recovered"])
print("Revenue recovered: ₹", metrics["total_recovered"])
print("Recovery rate:", round(metrics["recovery_rate"], 2), "%")


# Show how many decisions came from each source.
print("\nDecision summary:")

print(
    results["decision_source"]
    if "decision_source" in results.columns
    else "Decision source tracking will be added later."
)