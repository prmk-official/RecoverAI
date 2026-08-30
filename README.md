# RecoverAI

### AI-Assisted Payment Recovery for Failed Transactions

RecoverAI is an experimental payment-recovery system that explores how AI-assisted reasoning can improve decisions around failed payments.

The project uses a **hybrid approach**:

- Deterministic Python rules handle straightforward cases.
- Gemini provides contextual reasoning for cases that require additional judgment.
- A Python safety layer validates the proposed action before execution.
- A simulator models the outcome of the selected recovery action.
- Audit logs and evaluation metrics are used to compare recovery strategies.
- A Streamlit dashboard visualizes the results.

The project was built around a payment-recovery problem relevant to **Razorpay**, as part of my exploration of practical applications of AI in payment systems.

> **Important:** RecoverAI is an experimental prototype. It uses synthetic payment data and a simulated payment environment. It is not an official Razorpay product or integration and does not process real customer payments.

---

## Why I Built This

Failed payments are not all the same.

A payment that fails because of an expired card should not necessarily be treated the same way as a temporary bank error or an insufficient-funds failure.

I wanted to explore whether recovery decisions could be made more intelligently by combining:

1. predictable rules for cases that can be handled deterministically, and
2. AI-assisted reasoning for cases where additional payment and customer context may matter.

Building RecoverAI also gave me an opportunity to understand how an AI component can be incorporated into a system **without giving the model unrestricted control over important actions**.

---

## The Problem

A simple payment-retry system might repeatedly attempt to recover a failed payment.

However, different failure conditions can require different actions.

For example:

| Situation | Possible action |
|---|---|
| Expired card | Request a new payment method |
| Maximum retry limit reached | Stop and escalate |
| Temporary bank error | Retry |
| Timeout | Review |
| Insufficient funds + strong payment history | Consider retrying |
| Insufficient funds + weak history/repeated failures | Request another payment method |

The challenge is deciding **which action makes sense for each failed payment**.

---

# How RecoverAI Works

The system follows this workflow:

```text
                  Failed Payment
                        │
                        ▼
             ┌─────────────────────┐
             │ Deterministic Rules │
             │      (Python)       │
             └──────────┬──────────┘
                        │
             Straightforward case?
                  ┌─────┴─────┐
                 YES          NO
                  │            │
                  ▼            ▼
              Decision      Gemini
                           Reasoning
                              │
                              ▼
                    Recovery Decision
                              │
                              ▼
                  ┌───────────────────┐
                  │ Python Safety     │
                  │    Validation     │
                  └─────────┬─────────┘
                            │
                            ▼
                    Approved Action
                            │
                            ▼
                     Payment Simulator
                            │
                            ▼
                       Result
                            │
                            ▼
                  Audit + Evaluation
                            │
                            ▼
                       Dashboard