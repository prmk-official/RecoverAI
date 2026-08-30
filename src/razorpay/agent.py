import os
import json
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load the API key from the .env file.
load_dotenv()


@dataclass
class RecoveryDecision:
    """
    Stores one recovery decision.

    The same structure is used for both Python and Gemini
    decisions so the workflow can process them consistently.
    """

    # Recommended recovery action.
    action: str

    # Confidence in the recommendation, from 0 to 1.
    confidence: float

    # Explanation for the recommendation.
    reason: str

    # Identifies which component made the decision.
    source: str


# Create the Gemini client.
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Maximum number of Gemini requests allowed during one run.
# This protects us from exceeding the free-tier quota.
AI_CALL_LIMIT = 5


# Number of Gemini requests already made during this run.
ai_call_count = 0


def needs_ai_reasoning(payment):
    """
    Decide whether a payment needs AI reasoning.

    Straightforward cases are handled by Python.
    More ambiguous cases can be sent to Gemini.
    """

    failure = payment["failure_reason"]
    retries = payment["retry_count"]

    # Expired cards have an obvious solution.
    if failure == "expired_card":
        return False

    # Too many retries should never be handled by another
    # automatic retry.
    if retries >= 3:
        return False

    # Other cases may benefit from contextual reasoning.
    return True


def create_python_decision(payment):
    """
    Handle straightforward payment cases directly with Python.

    Returns a RecoveryDecision when Python knows the answer.

    Returns None when the case requires additional reasoning.
    """

    failure = payment["failure_reason"]
    retries = payment["retry_count"]

    # ---------------------------------------------------------
    # Expired card
    # ---------------------------------------------------------
    if failure == "expired_card":

        return RecoveryDecision(
            action="REQUEST_NEW_PAYMENT_METHOD",
            confidence=1.0,
            reason=(
                "The card is expired, so retrying the same "
                "card will not work."
            ),
        )

    # ---------------------------------------------------------
    # Maximum retry limit
    # ---------------------------------------------------------
    if retries >= 3:

        return RecoveryDecision(
            action="STOP_AND_ESCALATE",
            confidence=1.0,
            reason=(
                "The payment has already reached the "
                "maximum retry limit."
            ),
        )

    # Python does not have a deterministic answer.
    # Send the case to Gemini.
    return None


def ask_ai_for_decision(payment):
    """
    Ask Gemini to analyze a failed payment and return
    a structured recovery decision.

    The function has a per-run API limit and safely
    falls back to manual review if Gemini fails.
    """

    global ai_call_count

    # ---------------------------------------------------------
    # Check the Gemini request limit.
    # ---------------------------------------------------------
    if ai_call_count >= AI_CALL_LIMIT:

        return RecoveryDecision(
            action="REVIEW",
            confidence=1.0,
            reason=(
                "Gemini call limit reached; "
                "manual review required."
            ),
        )

    # Count the request before making the API call.
    ai_call_count += 1

    # ---------------------------------------------------------
    # Construct the AI prompt.
    # ---------------------------------------------------------
    prompt = f"""
You are a payment recovery decision assistant.

Analyze this failed payment:

{payment}

You may recommend ONLY one of these actions:

RETRY
REQUEST_NEW_PAYMENT_METHOD
STOP_AND_ESCALATE
REVIEW

Consider:
- failure reason
- retry count
- previous successful payments
- payment method
- customer status
- other available payment context

Return your answer as JSON with exactly these fields:

action
confidence
reason

Confidence must be a number between 0 and 1.
Reason should briefly explain the decision.
"""

    try:

        # -----------------------------------------------------
        # Send the request to Gemini.
        # -----------------------------------------------------
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                http_options=types.HttpOptions(
                    timeout=20_000
                ),
            ),
        )

        # -----------------------------------------------------
        # Convert Gemini's JSON response into a Python dict.
        # -----------------------------------------------------
        decision_data = json.loads(response.text)

        # -----------------------------------------------------
        # Validate the basic structure of the AI response.
        # -----------------------------------------------------
        action = decision_data["action"]
        confidence = float(decision_data["confidence"])
        reason = decision_data["reason"]

        # Keep confidence within the expected range.
        confidence = max(0.0, min(1.0, confidence))

        # -----------------------------------------------------
        # Return our standard decision object.
        # -----------------------------------------------------
        return RecoveryDecision(
            action=action,
            confidence=confidence,
            reason=reason,
        )

    except Exception as error:

        # -----------------------------------------------------
        # Gemini failure must not crash the payment workflow.
        # -----------------------------------------------------
        print(
            f"Gemini unavailable for "
            f"{payment['transaction_id']}: {error}"
        )

        # Safest fallback is manual review.
        return RecoveryDecision(
            action="REVIEW",
            confidence=1.0,
            reason=(
                "Gemini was unavailable; "
                "manual review required."
            ),
        )


def get_recovery_decision(payment):
    """
    Decide whether Python can handle the payment directly
    or whether Gemini should provide additional reasoning.

    Python handles deterministic cases first.
    Gemini handles ambiguous cases.
    """

    # ---------------------------------------------------------
    # Step 1: Try deterministic Python rules.
    # ---------------------------------------------------------
    python_decision = create_python_decision(payment)

    if python_decision is not None:
        return python_decision

    # ---------------------------------------------------------
    # Step 2: If Python cannot decide, use Gemini.
    # ---------------------------------------------------------
    return ask_ai_for_decision(payment)