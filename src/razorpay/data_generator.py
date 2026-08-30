import random
import pandas as pd


# Payment methods supported by our simulation.
PAYMENT_METHODS = ["card", "upi", "netbanking"]


def generate_failure_reason(payment_method):
    """
    Choose a realistic failure reason based on the payment method.
    """

    # Card payments can fail because of an expired card
    # or insufficient funds.
    if payment_method == "card":
        return random.choice([
            "insufficient_funds",
            "expired_card",
            "bank_error",
            "timeout",
        ])

    # UPI payments cannot have an expired card.
    elif payment_method == "upi":
        return random.choice([
            "insufficient_funds",
            "bank_error",
            "timeout",
        ])

    # Netbanking payments also cannot have an expired card.
    else:
        return random.choice([
            "bank_error",
            "timeout",
            "insufficient_funds",
        ])


def generate_payments(number_of_payments=500):
    """
    Generate synthetic failed-payment records.

    The data is designed to contain realistic relationships
    between payment methods and failure reasons.
    """

    payments = []

    # Generate each fake payment.
    for i in range(1, number_of_payments + 1):

        # Generate a random transaction amount.
        amount = random.choice([
            499, 799, 1299, 2499, 3499,
            4999, 5999, 8999, 12999, 24999
        ])

        # Choose the payment method first.
        payment_method = random.choice(PAYMENT_METHODS)

        # Choose a failure that makes sense for that method.
        failure_reason = generate_failure_reason(payment_method)

        # Generate customer history.
        previous_failures = random.randint(0, 4)
        previous_successes = random.randint(0, 12)

        # Generate previous retry attempts.
        retry_count = random.randint(0, 3)

        # Most customers are active.
        customer_status = random.choices(
            ["active", "inactive"],
            weights=[90, 10]
        )[0]

        # Store the payment information.
        payment = {
            "transaction_id": f"TXN{i:04d}",
            "customer_id": f"CUST{random.randint(1, 300):04d}",
            "amount": amount,
            "payment_method": payment_method,
            "failure_reason": failure_reason,
            "previous_failures": previous_failures,
            "previous_successes": previous_successes,
            "retry_count": retry_count,
            "customer_status": customer_status,
        }

        payments.append(payment)

    # Convert the payments into a Pandas DataFrame.
    return pd.DataFrame(payments)


# Generate 500 synthetic payments.
payments = generate_payments(500)

# Save the generated data.
payments.to_csv("data/payments.csv", index=False)

print("Generated", len(payments), "fake payments.")
print("Saved to data/payments.csv")