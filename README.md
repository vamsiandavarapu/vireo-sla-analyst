# ⚡ Vireo Audio — Support SLA Analyst (AI-Assisted Tool)

> **Weekly First-Response SLA Breach Report, Financial Impact Calculator & AI Root Cause Analyst**

---

## 📌 1. Deliverable 1: Working AI-Assisted Tool

This repository delivers a **working, end-to-end AI-assisted analytical web application** built with Python, Streamlit, Pandas, Plotly, and Gemini LLM integration.

### **Where is the tool in this project?**
1. **The Web Dashboard Application:** **[`app.py`](file:///f:/Project/Task1/app.py)**  
   - High-contrast Light Theme Streamlit interactive user interface.
   - Interactive metric cards, 1.3x enlarged Plotly visualizations, weekly breach trend line charts, agent leaderboard tables, shift breakdowns, and CSV data export.
2. **The AI Analyst Module:** **[`ai_analyst.py`](file:///f:/Project/Task1/ai_analyst.py)**  
   - Classifies unstructured customer messages & agent notes into operational delay themes (e.g., *Overnight Queue Carryover*, *Voice IVR Backlog*, *Refund Bottlenecks*).
   - Generates grounded, evidence-backed manager executive briefings for Support Operations Manager Neha Kulkarni.
3. **The Analytical Engine:** **[`sla_engine.py`](file:///f:/Project/Task1/sla_engine.py)**  
   - Deduplicates 11,816 raw records down to 11,200 unique tickets (616 duplicates removed).
   - Parses UTC timestamps and converts them to IST (Asia/Kolkata).
   - Time-matches historical agent rosters across 18 months.
   - Calculates exact SLA breach flags and ₹854,000 in store credit financial loss.
4. **The Automated Validation Suite:** **[`validate.py`](file:///f:/Project/Task1/validate.py)**  
   - Runs 16 automated test assertions verifying 100% mathematical accuracy against baseline policy metrics.

---

## 🚀 2. Clean Machine Setup Guide (Runs in 3 Steps)

Anyone on a brand new, clean machine can clone this repository and run the application in 3 simple steps:

### **Step 1: Install Dependencies**
Open terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### **Step 2: Run Automated Validation Test Suite**
Verify that all data calculations, breach counts, and financial exposure metrics match the baseline policy rules:
```bash
python validate.py
```
*Expected Output:*
```text
RESULTS: 16/16 Tests Passed (100.0%)
ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!
```

### **Step 3: Launch the Interactive Web Dashboard**
Run the Streamlit application:
```bash
streamlit run app.py
```
*The web app will automatically open in your browser at `https://vireo-sla-analyst.streamlit.app/`.*

---

## 📊 3. Key Verified Business Metrics

| Analytical Metric | Verified Value | Operational Context |
| :--- | :---: | :--- |
| **Raw Ticket Export Rows** | **11,816** | Initial raw export provided |
| **Unique Ticket IDs** | **11,200** | Post-deduplication (**616 migration duplicates removed**) |
| **Total SLA Breaches** | **2,440** | First response timestamp occurred later than SLA target |
| **Overall Breach Rate** | **21.79%** | ~21.8% baseline across all channels |
| **Total Financial Exposure** | **₹854,000** | 2,440 breaches × ₹350 store credit payout |
| **Tier 1 Morning Breach Rate** | **32.16%** | 1,866 breaches out of 5,803 tickets |
| **Morning Breaches Created Overnight** | **1,452** (**77.81%**) | **Root Cause Signal:** 77.81% of Morning breaches originated 22:00–06:00 IST |
| **Normal Hours Morning Breach Rate** | **11.02%** | Morning tickets created during shift hours (06:00–22:00 IST) |
| **Overnight Morning Breach Rate** | **70.93%** | Morning tickets created overnight (22:00–06:00 IST) |

---

## 🔒 4. Documented Analytical Assumptions & Scope Decisions

1. **Roster Matching Timestamp:** The dataset provides `agent_id` for the resolving agent, but lacks an `assigned_at` handoff timestamp. The engine uses the ticket creation timestamp (`created_at`) for consistent roster time-matching.
2. **Tier 2 Separation:** Tier 2 work is multi-touch and measured on resolution days, not volume first-response minutes. Tier 2 agents are excluded from volume first-response comparisons.
3. **Legacy CSAT:** CSAT score `0` in legacy Freshdesk rows is treated as a missing response (NaN) rather than zero score.
4. **Out-of-Scope Items:** Predictive ML breach models, vector databases, and multi-agent orchestration were intentionally excluded to focus strictly on deterministic accuracy within the 5-hour cap.

---
*Developed for Vireo Audio Support Operations Analytics Evaluation.*
