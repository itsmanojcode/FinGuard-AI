

````markdown
# 🛡️ FinGuard AI

### Defensive, Explainable & Bounded AI Finance Controller

FinGuard AI is an AI-powered merchant finance controller designed to help businesses monitor financial risk, investigate payment failures, recover at-risk revenue, detect anomalies, reconcile transactions, and maintain a complete audit trail.

The system combines **Razorpay Test Mode, FastAPI, Streamlit, AI agents, financial analytics, safety controls, and human approval workflows** into a single finance intelligence platform.

---

## 🚀 Key Features

### 💰 Revenue Recovery

FinGuard AI monitors failed Razorpay payments and identifies revenue at risk.

The system:

- Receives `payment.failed` webhook events
- Verifies Razorpay webhook signatures
- Stores payment failure information
- Calculates revenue at risk
- Evaluates recovery eligibility
- Routes high-value transactions for human approval
- Maintains recovery status and audit information

### 🤖 AI Finance Copilot

The AI Finance Copilot investigates financial questions using the finance intelligence pipeline.

It can analyze:

- Revenue leakage
- Refund behavior
- Transaction mismatches
- Financial anomalies
- Revenue risk
- Reconciliation exceptions

The workflow produces:

**Investigation → Decision → Safety Gate → Audit Trail**

### 🔄 Automated Reconciliation

FinGuard AI compares financial transaction data and identifies reconciliation mismatches.

It provides:

- Transaction matching
- Mismatch detection
- Unreconciled amount
- Exception identification

### 🚨 Anomaly Detection

The system detects unusual financial behavior using transaction analytics.

It can identify:

- Amount anomalies
- Unusual transactions
- Refund spikes
- Potential financial exposure

### 🛡️ Safety & Bounded Automation

FinGuard AI follows a defensive and bounded automation model.

High-risk actions are not executed blindly.

The system uses:

- Configurable financial limits
- Safety gates
- Human approval
- Manual review
- Explainable decisions
- Audit logging

### ✋ Human Approval Queue

Financial exceptions requiring human intervention are routed to an approval queue.

Reviewers can:

- Approve an action
- Reject an action
- View the financial amount
- View the AI decision
- View the reason for approval requirement

### 📜 Audit Trail

Important system and agent activities are recorded for traceability.

The dashboard provides visibility into:

- Agent execution
- Financial decisions
- Safety decisions
- Revenue recovery processing
- Webhook processing
- Audit events

---

# 🧠 System Architecture

```text
                         ┌─────────────────────┐
                         │      Razorpay       │
                         │     Test Mode       │
                         └──────────┬──────────┘
                                    │
                              payment.failed
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Razorpay Webhook  │
                         │   Signature Verify  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Payment Processor  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Revenue Recovery    │
                         │      Agent          │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
                ┌──────────────┐          ┌──────────────┐
                │ Risk / Rules │          │ AI Analysis  │
                └──────┬───────┘          └──────┬───────┘
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Safety Gate      │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  ▼                 ▼                 ▼
             Auto Recovery     Approval Queue    Manual Review
                                    │
                                    ▼
                            Human Decision
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Audit Trail      │
                         └─────────────────────┘
````

---

# 📊 Dashboard

FinGuard AI provides a unified Streamlit dashboard containing:

* Gross Revenue
* Net Revenue
* Refunds
* Reconciliation Exceptions
* Revenue At Risk
* Auto Recovery
* Failed Payments
* Anomalies
* AI Investigation
* Agent Activity
* Human Approvals
* Audit Trail

---

# 🧩 Application Modules

The application contains the following major sections:

### Dashboard

Provides an overall financial health summary.

### Revenue Recovery

Shows failed Razorpay payments and recovery decisions.

### Reconciliation

Displays transaction mismatches and unreconciled amounts.

### Anomalies

Highlights unusual financial transactions and refund spikes.

### AI Finance Copilot

Allows users to ask financial questions and receive AI-powered investigation and decisions.

### Agent Activity

Shows the execution status of the finance intelligence pipeline.

### Approvals

Provides a human-in-the-loop approval queue for financial exceptions.

### Audit Trail

Provides visibility into financial and agent decisions.

---

# 🔐 Webhook Security

Razorpay webhook requests are verified using **HMAC SHA-256**.

The system:

1. Reads the raw webhook request body.
2. Reads the `X-Razorpay-Signature` header.
3. Generates an HMAC SHA-256 digest.
4. Compares the generated signature with Razorpay's signature.
5. Rejects requests with invalid signatures.

Invalid webhook requests return:

```text
401 Invalid signature
```

---

# ♻️ Duplicate Webhook Protection

FinGuard AI prevents duplicate processing of the same Razorpay webhook event.

The system uses the Razorpay event ID to detect previously processed events.

Duplicate events are ignored instead of creating duplicate financial records.

Example response:

```json
{
  "status": "duplicate_ignored"
}
```

---

# 💡 Revenue Recovery Logic

Failed payments are categorized into bounded recovery paths:

```text
                 Failed Payment
                       │
                       ▼
                Risk Evaluation
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Auto Recovery  Approval     Manual Review
                    Required
```

The dashboard displays:

* Revenue At Risk
* Auto Recovery Amount
* Approval Required Amount
* Manual Review Amount

---

# 🛡️ Safety Model

FinGuard AI follows the principle:

> **AI recommends, safety controls constrain, humans approve high-risk actions.**

The system is designed to avoid unrestricted autonomous financial actions.

High-value or sensitive actions can be routed through:

```text
AI Decision
     ↓
Safety Gate
     ↓
Human Approval
     ↓
Approved / Rejected
     ↓
Audit Log
```

---

# 🧠 Agent Pipeline

The Finance Intelligence Pipeline consists of:

```text
Reconciliation Agent
        ↓
Anomaly Agent
        ↓
Finance Agent
        ↓
Decision Agent
        ↓
Safety Engine
        ↓
Audit Logging
```

The Revenue Recovery pipeline operates independently for failed Razorpay payments:

```text
Webhook Listener
        ↓
Payment Failure Processor
        ↓
Revenue Recovery Agent
        ↓
Risk Evaluation
        ↓
Recovery Decision
        ↓
Human Approval Gate
        ↓
Audit Logging
```

---

# 🛠️ Technology Stack

| Technology        | Purpose                      |
| ----------------- | ---------------------------- |
| Python            | Core application logic       |
| Streamlit         | Interactive dashboard        |
| FastAPI           | Backend API                  |
| SQLAlchemy        | Database ORM                 |
| SQLite            | Local database               |
| Pandas            | Financial data processing    |
| Plotly            | Data visualization           |
| Razorpay          | Payment event integration    |
| HMAC SHA-256      | Webhook security             |
| Gemini AI         | Financial investigation      |
| LangGraph         | Agent workflow orchestration |
| Cloudflare Tunnel | Local webhook exposure       |
| Pytest            | Testing                      |

---

# 📁 Project Structure

```text
FinGuard-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── backend/
│   ├── api/
│   │   ├── server.py
│   │   └── routes.py
│   │
│   ├── agents/
│   │   └── revenue_agent.py
│   │
│   ├── analytics/
│   │   ├── anomaly.py
│   │   ├── reconciliation.py
│   │   └── revenue.py
│   │
│   ├── data/
│   │   └── generator.py
│   │
│   ├── graph/
│   │   └── finance_graph.py
│   │
│   ├── services/
│   │   ├── audit_service.py
│   │   └── event_processor.py
│   │
│   ├── config.py
│   ├── database.py
│   └── models.py
│
└── tests/
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FinGuard-AI
```

## 2. Create virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file from the example:

### Windows

```powershell
copy .env.example .env
```

Configure the required environment variables:

```env
DATABASE_URL=sqlite:///finguard.db

GEMINI_API_KEY=your_gemini_api_key

RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

AUTO_ACTION_LIMIT=1000
APPROVAL_LIMIT=5000
```

> ⚠️ Never commit `.env` or real API credentials to GitHub.

---

# ▶️ Running the Application

## Start Streamlit Dashboard

```powershell
python -m streamlit run app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

## Start FastAPI Backend

In a separate terminal:

```powershell
uvicorn backend.api.server:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

---

# 🌐 Razorpay Webhook Testing

For local development, expose the FastAPI server using Cloudflare Tunnel:

```powershell
cloudflared tunnel --url http://localhost:8000
```

Cloudflare will generate a temporary public URL.

Configure the Razorpay webhook endpoint as:

```text
https://YOUR-TUNNEL-URL/api/webhooks/razorpay
```

Use **Razorpay Test Mode** for development and demonstration.

---

# 🧪 Testing

Run the automated test suite:

```powershell
pytest
```

---

# 🔄 Example End-to-End Flow

A typical failed payment workflow:

```text
1. Customer payment fails
          ↓
2. Razorpay generates payment.failed
          ↓
3. Webhook reaches FinGuard AI
          ↓
4. Signature is verified
          ↓
5. Duplicate event is checked
          ↓
6. Payment is stored
          ↓
7. Revenue Recovery Agent analyzes failure
          ↓
8. Risk / recovery status is calculated
          ↓
9. High-value actions can require human approval
          ↓
10. Decision is recorded in audit trail
          ↓
11. Dashboard displays revenue impact
```

---

# 🎯 Example Demo Scenario

FinGuard AI can be demonstrated using Razorpay Test Mode.

### Scenario

A payment failure occurs for a merchant transaction.

The system detects:

```text
Payment Status: Failed
Revenue At Risk: ₹500
Recovery Status: Eligible
```

The dashboard then displays the transaction under Revenue Recovery.

For higher-value transactions, the system can route the action to:

```text
Human Approval Queue
```

This demonstrates bounded automation rather than unrestricted financial execution.

---

# 🔒 Security Notes

* Use Razorpay **TEST credentials only** during the hackathon.
* Never expose API keys in source code.
* Never commit `.env`.
* Verify webhook signatures.
* Use HTTPS/public tunneling only for webhook testing.
* Keep financial actions bounded by configured limits.
* Require human approval for high-risk actions.

---

# 🏆 Why FinGuard AI?

Traditional finance dashboards mainly show what happened.

FinGuard AI focuses on:

```text
Detect
  ↓
Investigate
  ↓
Decide
  ↓
Constrain
  ↓
Approve
  ↓
Audit
```

This makes the system more than a monitoring dashboard — it acts as a **defensive finance intelligence and decision-support layer** for merchants.

---

# 🚧 Current Scope

FinGuard AI is currently designed as a **Razorpay Test Mode hackathon/buildathon prototype**.

The system demonstrates:

* Payment failure detection
* Revenue risk analysis
* AI-powered financial investigation
* Bounded recovery decisions
* Human-in-the-loop approvals
* Reconciliation
* Anomaly detection
* Auditability
* Webhook security
* Duplicate event protection

No real merchant funds are moved by the prototype.

---

# 🔮 Future Enhancements

Potential future improvements include:

* Multi-payment-provider support
* Production-grade PostgreSQL deployment
* Redis-based event processing
* Background task queues
* Advanced fraud detection
* Merchant-specific recovery strategies
* Email/SMS recovery workflows
* Automated retry orchestration
* Real-time financial alerts
* Role-based access control
* Advanced agent observability
* Production deployment with persistent Cloudflare Tunnel

---

# 👨‍💻 Author

**Manoj Kumar**

FinGuard AI — AI-powered defensive finance controller.

---

## ⚠️ Disclaimer

This project is a hackathon/buildathon prototype intended for demonstration and experimentation.

It should not be used to make production financial decisions without appropriate security, compliance, testing, monitoring, and human oversight.

```

