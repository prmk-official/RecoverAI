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

st.markdown(
    dedent(
        """
        <style>
        /* ---------- Global ---------- */
        .stApp {
            background:
                radial-gradient(circle at 88% 4%, rgba(124, 58, 237, .20), transparent 28%),
                radial-gradient(circle at 5% 35%, rgba(6, 182, 212, .10), transparent 25%),
                #080b18;
            color: #f8fafc;
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
            background: linear-gradient(180deg, #0d1024 0%, #080b18 100%);
            border-right: 1px solid rgba(139, 92, 246, .20);
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
            background: linear-gradient(90deg, #fff, #a855f7, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sidebar-subtitle {
            color: #94a3b8;
            font-size: 12px;
            margin-top: 5px;
        }

        .sidebar-nav {
            color: #cbd5e1;
            line-height: 2.5;
            font-size: 13px;
        }

        .sidebar-quote {
            margin-top: 45px;
            padding: 17px;
            border-radius: 16px;
            border: 1px solid rgba(168, 85, 247, .35);
            background: rgba(15, 23, 42, .75);
            color: #cbd5e1;
            font-size: 13px;
            line-height: 1.7;
        }

        /* ---------- Hero ---------- */
        .hero {
            padding: 8px 0 25px;
        }

        .hero-small {
            color: #a78bfa;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .hero-title {
            font-size: 52px;
            font-weight: 850;
            line-height: 1.05;
            margin: 2px 0 8px;
            background: linear-gradient(90deg, #fff, #c084fc 48%, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-description {
            color: #94a3b8;
            font-size: 16px;
            max-width: 760px;
            line-height: 1.6;
        }

        .hero-badge {
            display: inline-block;
            margin-top: 14px;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(34, 211, 238, .09);
            border: 1px solid rgba(34, 211, 238, .25);
            color: #67e8f9;
            font-size: 12px;
            font-weight: 700;
        }

        /* ---------- Sections ---------- */
        .section-title {
            font-size: 23px;
            font-weight: 800;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #f8fafc;
        }

        /* ---------- KPI cards ---------- */
        .metric-card {
            min-height: 145px;
            padding: 20px;
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(20, 27, 52, .96), rgba(12, 16, 34, .96));
            border: 1px solid rgba(148, 163, 184, .12);
            box-shadow: 0 10px 30px rgba(0, 0, 0, .20);
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
            background: rgba(168, 85, 247, .16);
            filter: blur(4px);
        }

        .metric-icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .metric-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 650;
        }

        .metric-value {
            color: #fff;
            font-size: 29px;
            font-weight: 850;
            margin-top: 5px;
        }

        .metric-change {
            color: #4ade80;
            font-size: 12px;
            font-weight: 700;
            margin-top: 5px;
        }

        .purple { border-top: 2px solid #a855f7; }
        .pink { border-top: 2px solid #ec4899; }
        .cyan { border-top: 2px solid #22d3ee; }
        .green { border-top: 2px solid #22c55e; }

        /* ---------- Comparison ---------- */
        .comparison {
            padding: 24px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(25, 20, 55, .96), rgba(10, 18, 35, .96));
            border: 1px solid rgba(139, 92, 246, .25);
            box-shadow: 0 12px 35px rgba(0, 0, 0, .22);
        }

        .comparison-label {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 5px;
        }

        .comparison-value {
            font-size: 38px;
            font-weight: 850;
        }

        .baseline-value { color: #c084fc; }
        .ai-value { color: #4ade80; }

        .progress-bg {
            width: 100%;
            height: 9px;
            background: #1e293b;
            border-radius: 99px;
            overflow: hidden;
            margin-top: 12px;
        }

        .progress-purple {
            height: 100%;
            background: linear-gradient(90deg, #7c3aed, #c084fc);
            border-radius: 99px;
        }

        .progress-green {
            height: 100%;
            background: linear-gradient(90deg, #16a34a, #4ade80);
            border-radius: 99px;
        }

        /* ---------- Insight cards ---------- */
        .insight-card {
            padding: 19px;
            min-height: 135px;
            border-radius: 18px;
            background: rgba(15, 23, 42, .82);
            border: 1px solid rgba(148, 163, 184, .12);
        }

        .insight-heading {
            font-size: 16px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 9px;
        }

        .insight-text {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.65;
        }

        .highlight {
            color: #4ade80;
            font-weight: 800;
        }

        /* ---------- Table ---------- */
        .transaction-wrapper {
            border-radius: 18px;
            overflow-x: auto;
            border: 1px solid rgba(148, 163, 184, .12);
            background: rgba(15, 23, 42, .80);
        }

        .transaction-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            min-width: 850px;
        }

        .transaction-table th {
            text-align: left;
            padding: 13px;
            color: #94a3b8;
            background: #111827;
            border-bottom: 1px solid #1e293b;
            white-space: nowrap;
        }

        .transaction-table td {
            padding: 13px;
            color: #cbd5e1;
            border-bottom: 1px solid rgba(51, 65, 85, .45);
        }

        .transaction-table tr:hover {
            background: rgba(124, 58, 237, .08);
        }

        .recovered {
            color: #4ade80 !important;
            font-weight: 750;
        }

        .badge {
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: 800;
        }

        .badge-green {
            background: rgba(34, 197, 94, .13);
            color: #4ade80;
        }

        .badge-red {
            background: rgba(244, 63, 94, .13);
            color: #fb7185;
        }

        /* ---------- Footer ---------- */
        .custom-footer {
            margin-top: 55px;
            padding: 23px;
            text-align: center;
            border-radius: 18px;
            border: 1px solid rgba(168, 85, 247, .25);
            background: linear-gradient(90deg, rgba(88, 28, 135, .18), rgba(14, 116, 144, .18));
        }

        .footer-title {
            color: #f8fafc;
            font-weight: 800;
            font-size: 16px;
        }

        .footer-text {
            color: #64748b;
            font-size: 12px;
            margin-top: 6px;
        }
        </style>
        """
    ),
    unsafe_allow_html=True,
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
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="sidebar-quote">
                <b>Smarter decisions.</b><br>
                Higher recoveries.<br>
                Better outcomes. ✨
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
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
    unsafe_allow_html=True,
)


# =========================================================
# RECOVERY OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Recovery Overview</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )


# =========================================================
# RECOVERY RATE COMPARISON
# =========================================================

st.markdown(
    '<div class="section-title">Recovery Rate Comparison</div>',
    unsafe_allow_html=True,
)

st.markdown(
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

                    <div style="color:#64748b;font-size:11px;margin-top:8px;">
                        {baseline_recovered_count:,} payments recovered
                    </div>
                </div>

                <div style="
                    width:12%;
                    text-align:center;
                    font-size:20px;
                    font-weight:800;
                    color:#64748b;">
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

                    <div style="color:#64748b;font-size:11px;margin-top:8px;">
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
    unsafe_allow_html=True,
)


# =========================================================
# PAYMENT ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-title">Payment Analytics</div>',
    unsafe_allow_html=True,
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
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
    st.markdown(
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
        ),
        unsafe_allow_html=True,
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

st.markdown(
    '<div class="section-title">Key Insights</div>',
    unsafe_allow_html=True,
)

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

with insight2:
    top_failure_counts = payments["failure_reason"].value_counts()
    top_failure = top_failure_counts.idxmax()
    top_failure_count = top_failure_counts.max()

    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )

with insight3:
    st.markdown(
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
        ),
        unsafe_allow_html=True,
    )


# =========================================================
# TRANSACTION EXPLORER
# =========================================================

st.markdown(
    '<div class="section-title">Transaction Explorer</div>',
    unsafe_allow_html=True,
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

table = filtered[available_columns].head(25)

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

st.markdown(
    html,
    unsafe_allow_html=True,
)

st.caption(
    f"Showing {min(len(filtered), 25)} "
    f"of {len(filtered)} matching transactions."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
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
                    Purvika Reddy
                </b>
                · Turning failed payments into smarter recovery decisions ✨
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)
