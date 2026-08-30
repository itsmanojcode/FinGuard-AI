import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from backend.database import init_db
from backend.data.generator import generate_transactions
from backend.analytics.reconciliation import reconcile_dataframe
from backend.analytics.anomaly import detect_anomalies, detect_refund_spike
from backend.analytics.revenue import calculate_revenue
from backend.graph.finance_graph import build_graph


# ============================================================
# CONFIGURATION
# ============================================================

#API_URL = "http://127.0.0.1:8000"
API_URL = "https://finguard-ai-u8ha.onrender.com"


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="FinGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

init_db()

#new adding part

if "approval_queue" not in st.session_state:
    st.session_state.approval_queue = []


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ FinGuard AI")

st.caption(
    "Autonomous Finance Controller — "
    "defensive, explainable and bounded"
)


# ============================================================
# DEMO FINANCIAL DATA
# ============================================================

if "data" not in st.session_state:
    st.session_state.data = generate_transactions(1000)


df = st.session_state.data.copy()


# ============================================================
# EXISTING ANALYTICS
# ============================================================

rec = reconcile_dataframe(df)
rev = calculate_revenue(df)


# ============================================================
# API HELPER FUNCTIONS
# ============================================================

def get_revenue_risk():

    try:

        response = requests.get(
            f"{API_URL}/api/revenue-risk",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e),
            "failed_payments": 0,
            "total_revenue_at_risk": 0,
            "auto_recovery_amount": 0,
            "approval_required_amount": 0,
            "manual_review_amount": 0
        }


def get_failed_payments():

    try:

        response = requests.get(
            f"{API_URL}/api/payments/failed",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return []


def get_all_payments():

    try:

        response = requests.get(
            f"{API_URL}/api/payments",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return []


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Revenue Recovery",
        "Reconciliation",
        "Anomalies",
        "AI Finance Copilot",
        "Agent Activity",
        "Approvals",
        "Audit Trail"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Financial Overview")

    # --------------------------------------------
    # Financial Metrics
    # --------------------------------------------

    a, b, c, d = st.columns(4)

    a.metric(
        "Gross Revenue",
        f"₹{rev['gross_revenue']:,.0f}"
    )

    b.metric(
        "Net Revenue",
        f"₹{rev['net_revenue']:,.0f}"
    )

    c.metric(
        "Refunds",
        f"₹{rev['refunds']:,.0f}"
    )

    d.metric(
        "Exceptions",
        int((rec["status"] == "MISMATCH").sum())
    )

    # --------------------------------------------
    # Charts
    # --------------------------------------------

    left, right = st.columns(2)

    with left:

        chart = pd.DataFrame(
            {
                "Category": [
                    "Gross",
                    "Refunds",
                    "Fees",
                    "Tax",
                    "Net"
                ],
                "Amount": [
                    rev["gross_revenue"],
                    rev["refunds"],
                    rev["fees"],
                    rev["tax"],
                    rev["net_revenue"]
                ]
            }
        )

        fig = px.bar(
            chart,
            x="Category",
            y="Amount",
            title="Revenue Breakdown"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        counts = (
            rec["status"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            counts,
            names="Status",
            values="Count",
            title="Reconciliation Status"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------
    # Refund Spike
    # --------------------------------------------

    info = detect_refund_spike(df)

    if info["is_spike"]:

        st.warning(
            f"⚠️ Refund spike detected. "
            f"Refund rate: {info['refund_rate']}%"
        )

    else:

        st.success(
            f"✅ Refund rate: {info['refund_rate']}%"
        )

    # --------------------------------------------
    # Razorpay Revenue Risk
    # --------------------------------------------

    st.divider()

    st.subheader("💰 Live Revenue Protection")

    risk = get_revenue_risk()

    if "error" not in risk:

        x, y, z = st.columns(3)

        x.metric(
            "Failed Payments",
            risk.get("failed_payments", 0)
        )

        y.metric(
            "Revenue At Risk",
            f"₹{risk.get('total_revenue_at_risk', 0):,.2f}"
        )

        z.metric(
            "Auto Recovery",
            f"₹{risk.get('auto_recovery_amount', 0):,.2f}"
        )

    else:

        st.info(
            "Razorpay revenue protection data "
            "is not available yet."
        )


# ============================================================
# REVENUE RECOVERY
# ============================================================

elif page == "Revenue Recovery":

    st.header("💰 Revenue Recovery Agent")

    st.caption(
        "AI-powered analysis of failed Razorpay payments "
        "and bounded recovery decisions."
    )

    # --------------------------------------------
    # Refresh
    # --------------------------------------------

    if st.button("🔄 Refresh Revenue Data"):

        st.rerun()

    # --------------------------------------------
    # Revenue Risk
    # --------------------------------------------

    risk = get_revenue_risk()

    if "error" in risk:

        st.error(
            "Unable to connect to FinGuard backend."
        )

        st.code(
            risk["error"]
        )

    else:

        # ----------------------------------------
        # Metrics
        # ----------------------------------------

        a, b, c, d = st.columns(4)

        a.metric(
            "Failed Payments",
            risk.get("failed_payments", 0)
        )

        b.metric(
            "Revenue At Risk",
            f"₹{risk.get('total_revenue_at_risk', 0):,.2f}"
        )

        c.metric(
            "Auto Recovery",
            f"₹{risk.get('auto_recovery_amount', 0):,.2f}"
        )

        d.metric(
            "Manual Review",
            f"₹{risk.get('manual_review_amount', 0):,.2f}"
        )

        st.divider()

        # ----------------------------------------
        # Recovery Categories
        # ----------------------------------------

        st.subheader("🎯 Recovery Decision Breakdown")

        x, y, z = st.columns(3)

        with x:

            st.success("🟢 Auto Recovery")

            st.metric(
                "Amount",
                f"₹{risk.get('auto_recovery_amount', 0):,.2f}"
            )

            st.caption(
                "Low-value transactions eligible "
                "for bounded automated recovery."
            )

        with y:

            st.warning("🟡 Approval Required")

            st.metric(
                "Amount",
                f"₹{risk.get('approval_required_amount', 0):,.2f}"
            )

            st.caption(
                "Human approval required before recovery."
            )

        with z:

            st.error("🔴 Manual Review")

            st.metric(
                "Amount",
                f"₹{risk.get('manual_review_amount', 0):,.2f}"
            )

            st.caption(
                "High-value transactions require "
                "manual investigation."
            )

        st.divider()

        # ----------------------------------------
        # Failed Payments
        # ----------------------------------------

        st.subheader("🚨 Failed Payment Analysis")

        failed_payments = get_failed_payments()

        if failed_payments:

            failed_df = pd.DataFrame(
                failed_payments
            )

            if "amount" in failed_df.columns:

                failed_df["amount"] = failed_df[
                    "amount"
                ].apply(
                    lambda x: f"₹{float(x):,.2f}"
                )

            st.dataframe(
                failed_df,
                width="stretch",
                hide_index=True
            )

        else:

            st.success(
                "🎉 No failed payments found."
            )

        st.divider()

        # ----------------------------------------
        # Recovery Explanation
        # ----------------------------------------

        st.subheader("🤖 FinGuard Decision Engine")

        total_risk = risk.get(
            "total_revenue_at_risk",
            0
        )

        auto_amount = risk.get(
            "auto_recovery_amount",
            0
        )

        approval_amount = risk.get(
            "approval_required_amount",
            0
        )

        manual_amount = risk.get(
            "manual_review_amount",
            0
        )

        if total_risk == 0:

            st.success(
                "FinGuard AI currently detects no "
                "revenue at risk from failed payments."
            )

        else:

            st.info(
                f"FinGuard AI detected "
                f"₹{total_risk:,.2f} of revenue at risk."
            )

            if auto_amount > 0:

                st.write(
                    f"🟢 ₹{auto_amount:,.2f} "
                    "can follow the automated recovery path."
                )

            if approval_amount > 0:

                st.write(
                    f"🟡 ₹{approval_amount:,.2f} "
                    "requires human approval."
                )

            if manual_amount > 0:

                st.write(
                    f"🔴 ₹{manual_amount:,.2f} "
                    "requires manual investigation."
                )

        st.divider()

        st.warning(
            "🛡️ Safety Policy: FinGuard AI does not "
            "directly move money. Recovery decisions "
            "are bounded by configured limits and "
            "high-value actions are routed for approval."
        )


# ============================================================
# RECONCILIATION
# ============================================================

elif page == "Reconciliation":

    st.header("🔄 Reconciliation")

    st.dataframe(
        rec,
        width="stretch"
    )

    x = rec[
        rec["status"] == "MISMATCH"
    ]

    st.metric(
        "Unreconciled Amount",
        f"₹{x['difference'].abs().sum():,.2f}"
    )


# ============================================================
# ANOMALIES
# ============================================================

elif page == "Anomalies":

    st.header("🚨 Anomalies")

    result = detect_anomalies(df)

    x = result[
        result["anomaly"]
    ]

    st.metric(
        "Amount Anomalies",
        len(x)
    )

    st.dataframe(
        x[
            [
                "payment_id",
                "amount",
                "refund",
                "settlement",
                "z_score"
            ]
        ],
        width="stretch"
    )


# ============================================================
# AI FINANCE COPILOT
# ============================================================

elif page == "AI Finance Copilot":

    st.header("🤖 AI Finance Copilot")

    st.caption(
        "Ask questions about revenue, refunds, "
        "fees, reconciliation and financial risk."
    )

    q = st.text_input(
        "Ask FinGuard",
        "Why is my revenue leaking?"
    )

    if st.button("🔍 Analyze"):

        with st.spinner(
            "FinGuard AI is investigating..."
        ):

            try:

                result = build_graph().invoke(
                    {
                        "data": df,
                        "question": q
                    }
                )

                # Save latest agent result
                st.session_state[
                    "last_agent_result"
                ] = result

                # ====================================================
                # ADD TO HUMAN APPROVAL QUEUE
                # ====================================================

                safety = result.get(
                    "safety_result",
                    {}
                )

                if safety.get("approval_required"):

                    reconciliation = result.get(
                        "reconciliation"
                    )

                    if reconciliation is not None:

                        mismatch_amount = float(
                            reconciliation.loc[
                                reconciliation["status"] == "MISMATCH",
                                "difference"
                            ].abs().sum()
                        )

                        if mismatch_amount > 0:

                            # Avoid duplicate approval requests
                            already_exists = any(
                                item.get("amount") == mismatch_amount
                                and item.get("status") == "Pending"
                                for item in st.session_state.approval_queue
                            )

                            if not already_exists:

                                st.session_state.approval_queue.append(
                                    {
                                        "type": "Reconciliation Exception",
                                        "amount": mismatch_amount,
                                        "status": "Pending",
                                        "decision": result.get(
                                            "decision",
                                            ""
                                        ),
                                        "reason": safety.get(
                                            "reason",
                                            "Human approval required"
                                        )
                                    }
                                )

                st.success(
                    "✅ Agent workflow completed successfully."
                )

            except Exception as e:

                st.error(
                    "❌ Agent workflow failed."
                )

                st.exception(e)

                result = None

        if result:

            st.divider()

            # ----------------------------------------
            # Investigation
            # ----------------------------------------

            st.subheader(
                "🔍 Investigation"
            )

            investigation = result.get(
                "investigation"
            )

            if investigation:

                st.markdown(
                    investigation
                )

            else:

                st.warning(
                    "No investigation result generated."
                )

            # ----------------------------------------
            # Decision
            # ----------------------------------------

            st.subheader(
                "🎯 Decision"
            )

            st.write(
                result.get(
                    "decision",
                    "No decision generated."
                )
            )

            # ----------------------------------------
            # Safety Gate
            # ----------------------------------------

            st.subheader(
                "🛡️ Safety Gate"
            )

            safety_result = result.get(
                "safety_result",
                {}
            )

            if safety_result.get("status") == "BLOCKED":

                st.error(
                    "🔴 ACTION BLOCKED — "
                    "Human approval required."
                )

            elif safety_result.get("status") == "APPROVAL_REQUIRED":

                st.warning(
                    "🟡 APPROVAL REQUIRED — "
                    "Human approval is needed."
                )

            elif safety_result.get("status"):

                st.success(
                    f"🟢 Safety status: "
                    f"{safety_result.get('status')}"
                )

            st.json(
                safety_result
            )

            # ----------------------------------------
            # Audit
            # ----------------------------------------

            st.subheader(
                "📜 Audit Trail"
            )

            st.json(
                result.get(
                    "audit_events",
                    []
                )
            )
            # ----------------------------------------
            # Decision
            # ----------------------------------------

            st.subheader(
                "🎯 Decision"
            )

            st.write(
                result.get(
                    "decision",
                    "No decision generated."
                )
            )

            # ----------------------------------------
            # Safety
            # ----------------------------------------

            st.subheader(
                "🛡️ Safety Gate"
            )

            safety_result = result.get(
                "safety_result",
                {}
            )

            if safety_result.get("status") == "BLOCKED":

                st.error(
                    "🔴 ACTION BLOCKED — Human approval required."
                )

            elif safety_result.get("status"):

                st.success(
                    f"🟢 Safety status: "
                    f"{safety_result.get('status')}"
                )

            st.json(
                safety_result
            )

            # ----------------------------------------
            # Audit
            # ----------------------------------------

            st.subheader(
                "📜 Audit Trail"
            )

            st.json(
                result.get(
                    "audit_events",
                    []
                )
            )


# ============================================================
# AGENT ACTIVITY
# ============================================================

elif page == "Agent Activity":

    st.header("🧠 Agent Activity")

    st.caption(
        "Live execution summary of the Finance Intelligence Pipeline."
    )

    result = st.session_state.get(
        "last_agent_result"
    )

    # IMPORTANT:
    # Everything below must remain INSIDE this elif block.

    if not result:

        st.info(
            "No agent workflow executed yet. "
            "Go to AI Finance Copilot and click Analyze."
        )

    else:

        # ============================================
        # PIPELINE HEADER
        # ============================================

        st.subheader(
            "Finance Intelligence Pipeline"
        )

        st.divider()

        # ============================================
        # RECONCILIATION AGENT
        # ============================================

        reconciliation = result.get(
            "reconciliation"
        )

        if reconciliation is not None:

            try:

                mismatch_count = int(
                    (
                        reconciliation["status"]
                        == "MISMATCH"
                    ).sum()
                )

                mismatch_amount = float(
                    reconciliation.loc[
                        reconciliation["status"]
                        == "MISMATCH",
                        "difference"
                    ].abs().sum()
                )

                if mismatch_count > 0:

                    st.warning(
                        f"🟡 Reconciliation Agent — Completed\n\n"
                        f"**{mismatch_count}** mismatches detected\n\n"
                        f"Unreconciled amount: "
                        f"**₹{mismatch_amount:,.2f}**"
                    )

                else:

                    st.success(
                        "🟢 Reconciliation Agent — "
                        "Completed successfully. No mismatches."
                    )

            except Exception:

                st.success(
                    "🟢 Reconciliation Agent — Completed"
                )

        # ============================================
        # ANOMALY AGENT
        # ============================================

        anomalies = result.get(
            "anomalies"
        )

        if anomalies is not None:

            try:

                anomaly_count = int(
                    anomalies["anomaly"].sum()
                )

                if anomaly_count > 0:

                    st.warning(
                        f"🟡 Anomaly Agent — "
                        f"{anomaly_count} anomalies detected"
                    )

                else:

                    st.success(
                        "🟢 Anomaly Agent — "
                        "Completed. 0 anomalies detected."
                    )

            except Exception:

                st.success(
                    "🟢 Anomaly Agent — Completed"
                )

        # ============================================
        # FINANCE AGENT
        # ============================================

        if result.get("investigation"):

            st.success(
                "🟢 Finance Agent — "
                "Gemini financial investigation completed"
            )

            with st.expander(
                "View Finance Agent Output"
            ):

                st.markdown(
                    result["investigation"]
                )

        # ============================================
        # DECISION AGENT
        # ============================================

        if result.get("decision"):

            st.info(
                "🔵 Decision Agent — Completed"
            )

            with st.expander(
                "View Decision"
            ):

                st.write(
                    result["decision"]
                )

        # ============================================
        # SAFETY GATE
        # ============================================

        safety = result.get(
            "safety_result",
            {}
        )

        if safety:

            status = safety.get(
                "status",
                "UNKNOWN"
            )

            if status == "BLOCKED":

                st.error(
                    f"🔴 Safety Gate — BLOCKED\n\n"
                    f"**Reason:** "
                    f"{safety.get('reason', 'Approval required')}"
                )

            else:

                st.success(
                    f"🟢 Safety Gate — {status}"
                )

        # ============================================
        # AUDIT AGENT
        # ============================================

        audit_events = result.get(
            "audit_events",
            []
        )

        if audit_events:

            st.success(
                f"🟢 Audit Agent — Completed\n\n"
                f"{len(audit_events)} audit event(s) recorded."
            )

        # ============================================
        # WORKFLOW SUMMARY
        # ============================================

        st.divider()

        st.subheader(
            "📈 Workflow Summary"
        )

        completed_agents = 0

        if reconciliation is not None:
            completed_agents += 1

        if anomalies is not None:
            completed_agents += 1

        if result.get("investigation"):
            completed_agents += 1

        if result.get("decision"):
            completed_agents += 1

        if safety:
            completed_agents += 1

        if audit_events:
            completed_agents += 1

        st.metric(
            "Agents Completed",
            f"{completed_agents}/6"
        )

        st.success(
            "✅ Finance Intelligence Pipeline completed."
        )

    # ============================================
    # REVENUE RECOVERY PIPELINE
    # ============================================

    st.divider()

    st.subheader(
        "💰 Revenue Recovery Pipeline"
    )

    recovery_activities = [
        (
            "🟢",
            "Razorpay Webhook Listener",
            "Receives payment events"
        ),
        (
            "🟢",
            "Payment Failure Processor",
            "Identifies failed transactions"
        ),
        (
            "🟢",
            "Revenue Recovery Agent",
            "Calculates recoverable revenue"
        ),
        (
            "🟢",
            "Risk Evaluation",
            "Evaluates financial exposure"
        ),
        (
            "🟢",
            "Recovery Decision",
            "Selects bounded recovery path"
        ),
        (
            "🟢",
            "Human Approval Gate",
            "Routes high-value actions for approval"
        ),
        (
            "🟢",
            "Audit Logging",
            "Records decisions and actions"
        )
    ]

    for icon, name, description in recovery_activities:

        with st.container(border=True):

            col1, col2 = st.columns(
                [1, 5]
            )

            with col1:

                st.markdown(
                    f"### {icon}"
                )

            with col2:

                st.markdown(
                    f"**{name}**"
                )

                st.caption(
                    description
                )


# ============================================================
# APPROVALS
# ============================================================

elif page == "Approvals":

    st.header("✋ Human Approval Queue")

    st.caption(
        "High-value or low-confidence financial actions "
        "require human approval before execution."
    )

    # ====================================================
    # RECONCILIATION APPROVALS
    # ====================================================

    st.subheader("🔐 Pending Financial Exceptions")

    queue = st.session_state.get(
        "approval_queue",
        []
    )

    pending = [
        item
        for item in queue
        if item["status"] == "Pending"
    ]

    if not pending:

        st.success(
            "✅ No financial exceptions are currently "
            "waiting for approval."
        )

    else:

        for index, item in enumerate(pending):

            with st.container(border=True):

                st.markdown(
                    f"### 🚨 {item['type']}"
                )

                a, b, c = st.columns(3)

                with a:

                    st.metric(
                        "Amount",
                        f"₹{item['amount']:,.2f}"
                    )

                with b:

                    st.metric(
                        "Status",
                        item["status"]
                    )

                with c:

                    st.metric(
                        "Risk Level",
                        "HIGH"
                    )

                st.divider()

                st.markdown(
                    "**AI Decision:**"
                )

                st.write(
                    item["decision"]
                )

                st.markdown(
                    "**Safety Reason:**"
                )

                st.warning(
                    item["reason"]
                )

                st.divider()

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{index}"
                    ):

                        item["status"] = "Approved"

                        item["approved_by"] = "Human Reviewer"

                        st.session_state[
                            "approval_queue"
                        ] = queue

                        st.success(
                            "Approval recorded successfully."
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{index}"
                    ):

                        item["status"] = "Rejected"

                        item["rejected_by"] = "Human Reviewer"

                        st.session_state[
                            "approval_queue"
                        ] = queue

                        st.warning(
                            "Exception rejected."
                        )

                        st.rerun()

    # ====================================================
    # APPROVAL SUMMARY
    # ====================================================

    st.divider()

    st.subheader("📊 Approval Summary")

    all_items = st.session_state.get(
        "approval_queue",
        []
    )

    pending_amount = sum(
        item["amount"]
        for item in all_items
        if item["status"] == "Pending"
    )

    approved_amount = sum(
        item["amount"]
        for item in all_items
        if item["status"] == "Approved"
    )

    rejected_amount = sum(
        item["amount"]
        for item in all_items
        if item["status"] == "Rejected"
    )

    a, b, c = st.columns(3)

    a.metric(
        "Pending",
        f"₹{pending_amount:,.2f}"
    )

    b.metric(
        "Approved",
        f"₹{approved_amount:,.2f}"
    )

    c.metric(
        "Rejected",
        f"₹{rejected_amount:,.2f}"
    )

    # ====================================================
    # RAZORPAY RECOVERY APPROVALS
    # ====================================================

    st.divider()

    st.subheader(
        "💰 Razorpay Revenue Recovery"
    )

    risk = get_revenue_risk()

    if "error" not in risk:

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "Revenue At Risk",
                f"₹{risk.get('total_revenue_at_risk', 0):,.2f}"
            )

        with b:

            st.metric(
                "Auto Recovery",
                f"₹{risk.get('auto_recovery_amount', 0):,.2f}"
            )

        with c:

            st.metric(
                "Razorpay Approval",
                f"₹{risk.get('approval_required_amount', 0):,.2f}"
            )

    else:

        st.info(
            "Razorpay recovery data is currently unavailable."
        )

    # ====================================================
    # SAFETY POLICY
    # ====================================================

    st.divider()

    st.info(
        "🛡️ Safety Policy: FinGuard AI never moves "
        "merchant funds autonomously for high-value "
        "or blocked actions. Human approval is required."
    )
# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.header("📜 Audit Trail")

    # First show actual agent audit events
    result = st.session_state.get(
        "last_agent_result"
    )

    if result and result.get("audit_events"):

        st.subheader(
            "🤖 Latest Agent Execution"
        )

        audit_events = result.get(
            "audit_events",
            []
        )

        st.json(
            audit_events
        )

    else:

        st.info(
            "No live agent execution audit is available yet."
        )

    st.divider()

    st.subheader(
        "📋 System Audit Components"
    )

    audit_data = pd.DataFrame(
        [
            {
                "Agent": "Reconciliation Agent",
                "Event": "Transaction matching",
                "Status": "Completed"
            },
            {
                "Agent": "Anomaly Agent",
                "Event": "Anomaly detection",
                "Status": "Completed"
            },
            {
                "Agent": "Finance Agent",
                "Event": "Gemini root-cause analysis",
                "Status": "Completed"
            },
            {
                "Agent": "Decision Agent",
                "Event": "Bounded financial decision",
                "Status": "Completed"
            },
            {
                "Agent": "Safety Engine",
                "Event": "Policy gate",
                "Status": "Completed"
            },
            {
                "Agent": "Revenue Recovery Agent",
                "Event": "Failed payment analysis",
                "Status": "Completed"
            },
            {
                "Agent": "Webhook Engine",
                "Event": "Razorpay event processing",
                "Status": "Completed"
            }
        ]
    )

    st.dataframe(
        audit_data,
        width="stretch",
        hide_index=True
    )