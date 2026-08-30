import random

# Use a fixed seed so our simulation produces
# the same results every time we run it.
random.seed(42)


def execute_action(payment, action):
    """
    Simulate the result of RecoverAI's chosen action.

    IMPORTANT:
    This does NOT process real payments.
    It only simulates possible outcomes for our project.
    """

    # Get useful information about this payment.
    successes = payment["previous_successes"]
    failures = payment["previous_failures"]
    amount = payment["amount"]

    # ---------------------------------------------------------
    # ACTION 1: RETRY
    # ---------------------------------------------------------
    if action == "RETRY":

        # Customers with a strong history are more likely
        # to successfully complete a retry.
        if successes >= 5:
            recovery_probability = 0.75
        else:
            recovery_probability = 0.40

        # Generate a random value between 0 and 1.
        if random.random() < recovery_probability:
            return "RECOVERED"

        return "FAILED"

    # ---------------------------------------------------------
    # ACTION 2: REQUEST NEW PAYMENT METHOD
    # ---------------------------------------------------------
    elif action == "REQUEST_NEW_PAYMENT_METHOD":

        # Simulate the customer updating their payment method.
        # We use a 65% chance for this example.
        if random.random() < 0.65:
            return "RECOVERED"

        return "CUSTOMER_DID_NOT_UPDATE"

    # ---------------------------------------------------------
    # ACTION 3: STOP AND ESCALATE
    # ---------------------------------------------------------
    elif action == "STOP_AND_ESCALATE":

        # We don't automatically charge the customer.
        # A human must handle the case.
        return "ESCALATED"

    # ---------------------------------------------------------
    # ACTION 4: MANUAL REVIEW
    # ---------------------------------------------------------
    elif action == "REVIEW":

        # Manual review means the AI does not automatically
        # take a financial action.
        return "MANUAL_REVIEW"

    # ---------------------------------------------------------
    # UNKNOWN ACTION
    # ---------------------------------------------------------
    else:
        return "NO_ACTION"