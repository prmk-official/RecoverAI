import pandas as pd
import streamlit as st
from textwrap import dedent


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RecoveryAI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.html(
    dedent(
        """
        <style>
        /* ---------- Global ---------- */
        .stApp {
            background: #f7f8fc;
            color: #27324a;
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e4e7ef;
        }

        .sidebar-brand {
            text-align: center;
            padding: 18px 5px 25px;
        }

        .sidebar-logo {
            font-size: 42px;
            margin-bottom: 4px;
        }

        .sidebar-title {
            font-size: 27px;
            font-weight: 800;
            background: none;
            
            color: #6652a8;
        }

        .sidebar-subtitle {
            color: #667085;
            font-size: 15px;
            margin-top: 5px;
        }

        .sidebar-nav {
            color: #526078;
            line-height: 2.5;
            font-size: 15px;
        }

        .sidebar-quote {
            margin-top: 45px;
            padding: 17px;
            border-radius: 16px;
            border: 1px solid #ddd2f4;
            background: #f7f5ff;
            color: #526078;
            font-size: 15px;
            line-height: 1.7;
        }

        /* ---------- Hero ---------- */
        .hero {
            padding: 8px 0 25px;
        }

        .hero-small {
            color: #7057b7;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .hero-title {
            font-size: 52px;
            font-weight: 850;
            line-height: 1.05;
            margin: 2px 0 8px;
            background: none;
            
            color: #6652a8;
        }

        .hero-description {
            color: #667085;
            font-size: 16px;
            max-width: 760px;
            line-height: 1.6;
        }

        .hero-badge {
            display: inline-block;
            margin-top: 14px;
            padding: 7px 13px;
            border-radius: 999px;
            background: #eef7ff;
            border: 1px solid #dbeafe;
            color: #5b7fc4;
            font-size: 15px;
            font-weight: 700;
        }

        /* ---------- Sections ---------- */
        .section-title {
            font-size: 23px;
            font-weight: 800;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #27324a;
        }

        /* ---------- KPI cards ---------- */
        .metric-card {
            min-height: 145px;
            padding: 20px;
            border-radius: 18px;
            background: #ffffff;
            border: 1px solid #e4e7ef;
            box-shadow: 0 8px 25px rgba(30, 41, 59, .06);
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            width: 100px;
            height: 100px;
            right: -40px;
            top: -40px;
            border-radius: 50%;
            background: #f7f5ff;
            filter: blur(4px);
        }

        .metric-icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .metric-label {
            color: #667085;
            font-size: 15px;
            font-weight: 650;
        }

        .metric-value {
            color: #27324a;
            font-size: 29px;
            font-weight: 850;
            margin-top: 5px;
        }

        .metric-change {
            color: #3b9b7a;
            font-size: 15px;
            font-weight: 700;
            margin-top: 5px;
        }

        .purple { border-top: 2px solid #9a83d5; }
        .pink { border-top: 2px solid #e7ad62; }
        .cyan { border-top: 2px solid #3b82f6; }
        .green { border-top: 2px solid #66b89a; }

        /* ---------- Comparison ---------- */
        .comparison {
            padding: 24px;
            border-radius: 20px;
            background: #ffffff;
            border: 1px solid #e4e7ef;
            box-shadow: 0 8px 25px rgba(30, 41, 59, .06);
        }

        .comparison-label {
            color: #667085;
            font-size: 15px;
            margin-bottom: 5px;
        }

        .comparison-value {
            font-size: 38px;
            font-weight: 850;
        }

        .baseline-value { color: #7c3aed; }
        .ai-value { color: #3b9b7a; }

        .progress-bg {
            width: 100%;
            height: 9px;
            background: #edf0f5;
            border-radius: 99px;
            overflow: hidden;
            margin-top: 12px;
        }

        .progress-purple {
            height: 100%;
            background: linear-gradient(90deg, #9a83d5, #b8a8e5);
            border-radius: 99px;
        }

        .progress-green {
            height: 100%;
            background: linear-gradient(90deg, #66b89a, #8bd0b4);
            border-radius: 99px;
        }

        /* ---------- Insight cards ---------- */
        .insight-card {
            padding: 19px;
            min-height: 135px;
            border-radius: 18px;
            background: #ffffff;
            border: 1px solid #e4e7ef;
        }

        .insight-heading {
            font-size: 16px;
            font-weight: 800;
            color: #27324a;
            margin-bottom: 9px;
        }

        .insight-text {
            color: #667085;
            font-size: 15px;
            line-height: 1.65;
        }

        .highlight {
            color: #3b9b7a;
            font-weight: 800;
        }

        /* ---------- Table ---------- */
        .transaction-wrapper {
            border-radius: 18px;
            overflow-x: auto;
            border: 1px solid #e4e7ef;
            background: #ffffff;
        }

        .transaction-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
            min-width: 850px;
        }

        .transaction-table th {
            text-align: left;
            padding: 13px;
            color: #667085;
            background: #f8fafc;
            border-bottom: 1px solid #e4e7ef;
            white-space: nowrap;
        }

        .transaction-table td {
            padding: 13px;
            color: #526078;
            border-bottom: 1px solid #edf0f5;
        }

        .transaction-table tr:hover {
            background: #f7f5ff;
        }

        .recovered {
            color: #3b9b7a !important;
            font-weight: 750;
        }

        .badge {
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: 800;
        }

        .badge-green {
            background: #dff5e9;
            color: #3b9b7a;
        }

        .badge-red {
            background: #fde7ed;
            color: #b85c77;
        }

        /* ---------- Footer ---------- */
        .custom-footer {
            margin-top: 55px;
            padding: 23px;
            text-align: center;
            border-radius: 18px;
            border: 1px solid #e4e7ef;
            background: linear-gradient(135deg, #ffffff, #f7f5ff);
        }

        .footer-title {
            color: #27324a;
            font-weight: 800;
            font-size: 16px;
        }

        .footer-text {
            color: #667085;
            font-size: 15px;
            margin-top: 6px;
        }


        /* ---------- Soft pastel page background ---------- */
        .stApp {
            background:
                radial-gradient(circle at 5% 5%, rgba(191, 177, 232, 0.22) 0, rgba(191, 177, 232, 0) 24%),
                radial-gradient(circle at 96% 8%, rgba(170, 211, 238, 0.22) 0, rgba(170, 211, 238, 0) 27%),
                radial-gradient(circle at 88% 78%, rgba(171, 222, 201, 0.18) 0, rgba(171, 222, 201, 0) 25%),
                linear-gradient(135deg, #f8f9fd 0%, #f3f6fb 48%, #f8f5fc 100%);
        }

        .main .block-container {
            background: rgba(255, 255, 255, 0.24);
            border-radius: 28px;
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }

        .main .block-container::before {
            content: "";
            position: fixed;
            width: 320px;
            height: 320px;
            right: -100px;
            top: 160px;
            border-radius: 50%;
            background: rgba(190, 174, 232, 0.10);
            filter: blur(35px);
            pointer-events: none;
            z-index: -1;
        }

        .main .block-container::after {
            content: "";
            position: fixed;
            width: 280px;
            height: 280px;
            left: -110px;
            bottom: 80px;
            border-radius: 50%;
            background: rgba(166, 210, 238, 0.10);
            filter: blur(35px);
            pointer-events: none;
            z-index: -1;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #f3effc 0%, #eef5fb 52%, #f1f8f4 100%);
            border-right: 1px solid #dedceb;
        }

        section[data-testid="stSidebar"] > div {
            background: transparent;
        }

        div[data-baseweb="select"] > div {
            border-radius: 12px;
            border-color: #d9ddea;
            background: rgba(255, 255, 255, 0.82);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }

        /* ---------- Pastel accents ---------- */
        .hero {
            background: linear-gradient(135deg, rgba(255,255,255,0.94) 0%, rgba(244,249,255,0.96) 52%, rgba(248,244,255,0.96) 100%);
            border-color: #e4e1ef;
        }

        .hero::after {
            background: rgba(154, 131, 213, 0.13);
        }

        .hero-pill {
            background: #fbfaff;
            border-color: #e2dcf5;
        }

        .metric-blue {
            background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
        }

        .metric-amber {
            background: linear-gradient(135deg, #ffffff 0%, #fffaf2 100%);
        }

        .metric-purple {
            background: linear-gradient(135deg, #ffffff 0%, #faf7ff 100%);
        }

        .metric-green {
            background: linear-gradient(135deg, #ffffff 0%, #f3fbf7 100%);
        }

        .icon-blue {
            background: #eaf4ff;
        }

        .icon-amber {
            background: #fff3df;
        }

        .icon-purple {
            background: #f1ebff;
        }

        .icon-green {
            background: #e5f7ef;
        }

        .side-card {
            background: linear-gradient(135deg, #f5f0ff 0%, #eef7ff 100%);
            border-color: #ddd4f1;
        }

        .comparison-card {
            background: linear-gradient(135deg, #ffffff 0%, #fbfaff 100%);
        }

        .progress-purple {
            background: linear-gradient(90deg, #9a83d5, #c2b3e8);
        }

        .progress-green {
            background: linear-gradient(90deg, #66b89a, #9ad8bf);
        }

        .insight-card:nth-child(1) {
            background: linear-gradient(135deg, #ffffff 0%, #f7f3ff 100%);
        }

        .insight-card:nth-child(2) {
            background: linear-gradient(135deg, #ffffff 0%, #fff8ef 100%);
        }

        .insight-card:nth-child(3) {
            background: linear-gradient(135deg, #ffffff 0%, #f1fbf7 100%);
        }

        .insight-icon {
            background: #f1ebff;
        }

        .footer {
            background: linear-gradient(135deg, #ffffff 0%, #f7f5ff 100%);
            border-color: #e1dcef;
        }

        </style>
        """
    ),
)


# =========================================================
# LOAD DATA
# =========================================================

payments = pd.read_csv("data/payments.csv")
baseline = pd.read_csv("data/baseline_audit.csv")
ai_policy = pd.read_csv("data/ai_policy_audit.csv")


# =========================================================
# CALCULATE METRICS
# =========================================================

total_payments = len(payments)
total_at_risk = payments["amount"].sum()
baseline_recovered = baseline["recovered_amount"].sum()
ai_recovered = ai_policy["recovered_amount"].sum()

baseline_rate = (
    baseline_recovered / total_at_risk * 100
    if total_at_risk > 0 else 0
)

ai_rate = (
    ai_recovered / total_at_risk * 100
    if total_at_risk > 0 else 0
)

additional_revenue = ai_recovered - baseline_recovered
rate_improvement = ai_rate - baseline_rate

relative_improvement = (
    (ai_rate - baseline_rate) / baseline_rate * 100
    if baseline_rate > 0 else 0
)

baseline_recovered_count = int(
    (baseline["result"] == "RECOVERED").sum()
)

ai_recovered_count = int(
    (ai_policy["result"] == "RECOVERED").sum()
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.html(
        dedent(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">💳</div>
                <div class="sidebar-title">RecoveryAI</div>
                <div class="sidebar-subtitle">
                    AI-Powered Payment Recovery
                </div>
            </div>
            """
        )
    )

    st.divider()

    st.html(
        dedent(
            """
            <div class="sidebar-nav">
                📊 &nbsp; Dashboard<br>
                ◈ &nbsp; Overview<br>
                ◈ &nbsp; Analytics<br>
                ◈ &nbsp; Transactions<br>
                ◈ &nbsp; Insights
            </div>
            """
        )
    )

    st.html(
        dedent(
            """
            <div class="sidebar-quote">
                <b>Smarter decisions.</b><br>
                Higher recoveries.<br>
                Better outcomes. ✨
            </div>
            """
        )
    )


# =========================================================
# HERO
# =========================================================

st.html(
    dedent(
        """
        <div class="hero">
            <div class="hero-small">
                AI-POWERED PAYMENT RECOVERY
            </div>

            <div class="hero-title">
                RecoveryAI
            </div>

            <div class="hero-description">
                Turn failed payments into recovered revenue.
                RecoveryAI combines deterministic payment rules
                with AI-assisted reasoning to recommend smarter
                recovery actions.
            </div>

            <div class="hero-badge">
                ● Synthetic Payment Recovery Experiment
            </div>
        </div>
        """
    ),
)


# =========================================================
# RECOVERY OVERVIEW
# =========================================================

st.html(
    '<div class="section-title">Recovery Overview</div>',
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html(
        dedent(
            f"""
            <div class="metric-card purple">
                <div class="metric-icon">💳</div>
                <div class="metric-label">Total Payments</div>
                <div class="metric-value">{total_payments:,}</div>
                <div class="metric-change">
                    {ai_recovered_count:,} recovered by AI policy
                </div>
            </div>
            """
        )
    )

with col2:
    st.html(
        dedent(
            f"""
            <div class="metric-card pink">
                <div class="metric-icon">⚠️</div>
                <div class="metric-label">Revenue at Risk</div>
                <div class="metric-value">₹{total_at_risk:,.0f}</div>
                <div class="metric-change">
                    Failed-payment value analyzed
                </div>
            </div>
            """
        )
    )

with col3:
    st.html(
        dedent(
            f"""
            <div class="metric-card cyan">
                <div class="metric-icon">📈</div>
                <div class="metric-label">Baseline Recovered</div>
                <div class="metric-value">₹{baseline_recovered:,.0f}</div>
                <div class="metric-change">
                    {baseline_rate:.2f}% recovery rate
                </div>
            </div>
            """
        )
    )

with col4:
    st.html(
        dedent(
            f"""
            <div class="metric-card green">
                <div class="metric-icon">🚀</div>
                <div class="metric-label">AI-Informed Recovered</div>
                <div class="metric-value">₹{ai_recovered:,.0f}</div>
                <div class="metric-change">
                    ↑ ₹{additional_revenue:,.0f} vs baseline
                </div>
            </div>
            """
        )
    )


# =========================================================
# RECOVERY RATE COMPARISON
# =========================================================

st.html(
    '<div class="section-title">Recovery Rate Comparison</div>',
)

st.html(
    dedent(
        f"""
        <div class="comparison">

            <div style="color:#94a3b8;font-size:13px;margin-bottom:20px;">
                Python baseline vs AI-informed recovery policy
            </div>

            <div style="display:flex;align-items:center;">

                <div style="width:44%;">
                    <div class="comparison-label">
                        Python Baseline
                    </div>

                    <div class="comparison-value baseline-value">
                        {baseline_rate:.2f}%
                    </div>

                    <div class="progress-bg">
                        <div
                            class="progress-purple"
                            style="width:{min(baseline_rate, 100):.2f}%;">
                        </div>
                    </div>

                    <div style="color:#667085;font-size:11px;margin-top:8px;">
                        {baseline_recovered_count:,} payments recovered
                    </div>
                </div>

                <div style="
                    width:12%;
                    text-align:center;
                    font-size:22px;
                    font-weight:800;
                    color:#667085;">
                    VS
                </div>

                <div style="width:44%;">
                    <div class="comparison-label">
                        AI-Informed Policy
                    </div>

                    <div class="comparison-value ai-value">
                        {ai_rate:.2f}%
                    </div>

                    <div class="progress-bg">
                        <div
                            class="progress-green"
                            style="width:{min(ai_rate, 100):.2f}%;">
                        </div>
                    </div>

                    <div style="color:#667085;font-size:11px;margin-top:8px;">
                        {ai_recovered_count:,} payments recovered
                    </div>
                </div>

            </div>

            <div style="
                margin-top:24px;
                padding-top:17px;
                border-top:1px solid rgba(148,163,184,.12);
                color:#94a3b8;
                font-size:13px;">

                Recovery improved by
                <span style="color:#4ade80;font-weight:800;">
                    {rate_improvement:.2f} percentage points
                </span>
                with approximately
                <span style="color:#c084fc;font-weight:800;">
                    {relative_improvement:.0f}%
                </span>
                relative improvement over the baseline.

            </div>

        </div>
        """
    ),
)


# =========================================================
# PAYMENT ANALYTICS
# =========================================================

st.html(
    '<div class="section-title">Payment Analytics</div>',
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.html(
        dedent(
            """
            <div class="insight-card">
                <div class="insight-heading">
                    🔎 Failed Payment Breakdown
                </div>
                <div class="insight-text">
                    Number of failed payments grouped by failure reason.
                </div>
            </div>
            """
        )
    )

    failure_counts = (
        payments["failure_reason"]
        .value_counts()
        .rename_axis("Failure Reason")
        .to_frame("Payments")
    )

    st.bar_chart(
        failure_counts,
        height=300,
    )

with chart_col2:
    st.html(
        dedent(
            """
            <div class="insight-card">
                <div class="insight-heading">
                    💰 Revenue Recovered by Failure Type
                </div>
                <div class="insight-text">
                    Revenue recovered by the AI-informed policy for each
                    failure category.
                </div>
            </div>
            """
        )
    )

    recovery_by_failure = (
        ai_policy
        .groupby("failure_reason")["recovered_amount"]
        .sum()
        .sort_values(ascending=False)
        .to_frame("Recovered Revenue")
    )

    st.bar_chart(
        recovery_by_failure,
        height=300,
    )


# =========================================================
# KEY INSIGHTS
# =========================================================

st.html(
    '<div class="section-title">Key Insights</div>',
)

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.html(
        dedent(
            f"""
            <div class="insight-card">
                <div class="insight-heading">
                    ⭐ Revenue Impact
                </div>

                <div class="insight-text">
                    The AI-informed policy recovered
                    <span class="highlight">
                        ₹{additional_revenue:,.0f}
                    </span>
                    more revenue than the original Python baseline.
                </div>
            </div>
            """
        )
    )

with insight2:
    top_failure_counts = payments["failure_reason"].value_counts()
    top_failure = top_failure_counts.idxmax()
    top_failure_count = top_failure_counts.max()

    st.html(
        dedent(
            f"""
            <div class="insight-card">
                <div class="insight-heading">
                    🔥 Most Common Failure
                </div>

                <div class="insight-text">
                    <span class="highlight">
                        {top_failure}
                    </span>
                    was the most frequent failure, accounting for
                    <span class="highlight">
                        {top_failure_count}
                    </span>
                    payments.
                </div>
            </div>
            """
        )
    )

with insight3:
    st.html(
        dedent(
            f"""
            <div class="insight-card">
                <div class="insight-heading">
                    📊 Recovery Improvement
                </div>

                <div class="insight-text">
                    Recovery rate increased from
                    <span class="highlight">
                        {baseline_rate:.2f}%
                    </span>
                    to
                    <span class="highlight">
                        {ai_rate:.2f}%
                    </span>.
                </div>
            </div>
            """
        )
    )


# =========================================================
# TRANSACTION EXPLORER
# =========================================================

st.html(
    '<div class="section-title">Transaction Explorer</div>',
)

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    failure_options = (
        ["All"]
        + sorted(
            ai_policy["failure_reason"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_failure = st.selectbox(
        "Failure reason",
        failure_options,
    )

with filter_col2:
    result_options = (
        ["All"]
        + sorted(
            ai_policy["result"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_result = st.selectbox(
        "Recovery result",
        result_options,
    )


filtered = ai_policy.copy()

if selected_failure != "All":
    filtered = filtered[
        filtered["failure_reason"] == selected_failure
    ]

if selected_result != "All":
    filtered = filtered[
        filtered["result"] == selected_result
    ]


# =========================================================
# TRANSACTION TABLE
# =========================================================

display_columns = [
    "transaction_id",
    "amount",
    "failure_reason",
    "retry_count",
    "action",
    "reason",
    "result",
    "recovered_amount",
]

available_columns = [
    column
    for column in display_columns
    if column in filtered.columns
]

# Let the user control how many matching transactions are visible.
# The default remains 25 so the page stays compact, but all matching
# transactions can now be displayed.
if len(filtered) > 25:
    row_options = [25, 50, 100, 250, 500]
    row_options = [
        option for option in row_options
        if option <= len(filtered)
    ]

    if len(filtered) not in row_options:
        row_options.append(len(filtered))

    row_options = sorted(set(row_options))

    display_count = st.selectbox(
        "Transactions to display",
        row_options,
        index=0,
        format_func=lambda value: (
            f"{value} transactions"
            if value < len(filtered)
            else f"{value} transactions (all matching)"
        ),
    )
else:
    display_count = len(filtered)

if len(filtered) > 25:
    st.caption(
        "Use the selector above to view more transactions, "
        "including all matching records."
    )

table = filtered[available_columns].head(display_count)

html = """
<div class="transaction-wrapper">
<table class="transaction-table">
<thead>
<tr>
"""

for column in available_columns:
    nice_name = column.replace("_", " ").title()
    html += f"<th>{nice_name}</th>"

html += """
</tr>
</thead>
<tbody>
"""

for _, row in table.iterrows():

    html += "<tr>"

    for column in available_columns:

        value = row[column]

        if column == "amount":
            html += f"<td>₹{float(value):,.0f}</td>"

        elif column == "recovered_amount":

            formatted = f"₹{float(value):,.0f}"

            if float(value) > 0:
                html += (
                    f'<td class="recovered">{formatted}</td>'
                )
            else:
                html += f"<td>{formatted}</td>"

        elif column == "result":

            if value == "RECOVERED":
                html += (
                    "<td>"
                    '<span class="badge badge-green">'
                    "RECOVERED"
                    "</span>"
                    "</td>"
                )
            else:
                html += (
                    "<td>"
                    '<span class="badge badge-red">'
                    f"{value}"
                    "</span>"
                    "</td>"
                )

        else:
            html += f"<td>{value}</td>"

    html += "</tr>"

html += """
</tbody>
</table>
</div>
"""

st.html(
    html,
)

st.caption(
    f"Showing {len(table)} of {len(filtered)} matching transactions."
)


# =========================================================
# FOOTER
# =========================================================

st.html(
    dedent(
        """
        <div class="custom-footer">

            <div class="footer-title">
                💜 RecoveryAI
            </div>

            <div class="footer-text">
                AI-Assisted Payment Recovery System
                · Built with Python, Gemini & Streamlit
            </div>

            <div class="footer-text" style="margin-top:12px;">
                Created by
                <b style="color:#c084fc;">
                    Purvika Reddy MK
                </b>
                · Turning failed payments into smarter recovery decisions ✨
            </div>

        </div>
        """
    ),
)
