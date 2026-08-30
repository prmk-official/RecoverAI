import pandas as pd


def save_audit_log(results, filename="data/audit_log.csv"):
    """
    Save the decisions and outcomes of our recovery system.

    This creates an audit trail so we can later understand
    exactly what happened to each payment.
    """

    # Convert our list of results into a Pandas table.
    audit_data = pd.DataFrame(results)

    # Save the table as a CSV file.
    audit_data.to_csv(filename, index=False)

    print(f"Audit log saved to {filename}")