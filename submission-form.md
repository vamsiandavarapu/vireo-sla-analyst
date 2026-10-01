# VIREO AUDIO — SUPPORT SLA ANALYST SUBMISSION FORM

### 1. What did we build, and what business outcome does it move?
We built a reproducible, deterministic SLA analytical engine paired with an interactive Streamlit web dashboard (`app.py`) and a controlled AI narrative layer (`ai_analyst.py`). 
- **Business Outcome:** It addresses the client's core request (Neha Kulkarni's demand for weekly SLA breach reports by agent and shift). It identifies an overall breach rate of **21.79%** across 11,200 unique tickets, representing **Rs 854,000** in store credit financial loss. 
- **Target Impact:** Reducing the breach rate to the proposed **15.0% target** recovers roughly **Rs 201,000 per quarter** (~Rs 15.4k/week) in avoided SLA store credit payouts. It also uncovers the root cause: **77.81%** of Morning shift breaches stem from overnight ticket carryover (22:00 – 06:00 IST), preventing unfair penalties on morning agents.

---

### 2. What does one run cost, and what would a month cost at roughly 650 tickets/week? Show arithmetic.
- **Deterministic Analytics Engine:** **Rs 0.00** (Runs 100% locally via Python/Pandas).
- **AI Classification & Narrative Layer:**
  - Standard Mode (Offline / Rule-based Heuristic Engine): **Rs 0.00 / month**.
  - LLM API Mode (Gemini 1.5 Flash):
    - Input tokens per run (~50 sampled tickets + prompt): ~3,500 tokens @ $0.075 / 1M tokens = $0.00026 (~Rs 0.022).
    - Output tokens per run: ~500 tokens @ $0.30 / 1M tokens = $0.00015 (~Rs 0.012).
    - **Cost per weekly run:** ~$0.00041 (~Rs 0.034).
    - **Cost per month (4 weekly runs @ 650 tickets/week):** ~$0.0016 (~**Rs 0.14 per month**).

---

### 3. How do we know it works? Sample size, checking method, error rate and wrong-case type.
- **Verification Suite (`validate.py`):** 16 automated assertions were run against the 11,816 raw dataset rows.
- **Sample & Error Rate:**
  - Tested 100% of 11,816 raw ticket rows for deduplication (616 duplicate rows correctly identified and dropped).
  - Manually verified exact boundary cases (e.g. Chat response at exactly 15m00s = Within SLA; 15m01s = Breach).
  - Timezone parsing verified: UTC timestamps accurately converted to IST (+5:30).
  - Deterministic engine error rate: **0.0%**.
  - AI text classification error rate on sample (n=50): ~4.0% (mainly on ambiguous/failed IVR transcripts where text was corrupted or empty).

---

### 4. Did we change, narrow or push back on the client's ask? What, when and why?
- **Pushed Back on Causal Claim:** The client's initial email thread suggested that the June roster reshuffle caused morning agent underperformance. We pushed back by framing the June movement as a diagnostic signal rather than proof of causation, proving mathematically that 77.81% of Morning breaches were accumulated overnight before the shift began.
- **Narrowed Scope on Target:** Treated the 15% breach rate as a proposed project target for financial modeling rather than an established policy contract.
- **Scope Alignment:** Kept the tool focused strictly on deterministic weekly agent/shift SLA breach reporting without over-engineering complex ML/RAG architectures.

---

### 5. What is wrong with what we are handing over? Specific bugs, shortcuts and known gaps.
- **Roster Timestamp Assumption:** The supplied CSVs lack an `assigned_at` handoff timestamp. Roster mapping uses ticket `created_at` time. Tickets spanning roster changes attribute breaches to the resolving agent's roster row at creation.
- **Tier 2 Metrics:** Tier 2 resolution is measured in days, not first-response minutes. They are excluded from volume SLA comparisons.
- **Failed IVR Transcripts:** ~40 raw IVR records contain low-quality speech-to-text transcripts which may cause minor misclassifications in AI text categorization.

---

### 6. What did we deliberately leave out, and why?
- **Predictive ML Breach Models:** Not needed to answer Neha's weekly historical reporting ask.
- **Vector DB / RAG Pipeline:** Over-engineered for a 5-hour analytical assignment; deterministic Pandas aggregations are faster and 100% accurate.
- **Automated Staffing Re-allocation Engine:** Staffing is frozen until Q4 per Finance directives.

---

### 7. Anything useful we built/found beyond the ask?
- **Overnight Creation Signal Decomposition:** Discovered that Morning shift tickets created in-shift have only an **11.02%** breach rate, whereas overnight-created tickets have a **70.93%** breach rate.
- **Financial Exposure Calculator:** Added real-time quarterly financial savings modeling based on configurable breach targets.

---

### 8. What AI tools/models were used, where they helped, where they wasted time and what was discarded?
- **Models Used:** Gemini 1.5 Flash (via Google Generative AI Python SDK) + Grounded Rule-based Fallback.
- **Where AI Helped:** Summarizing customer complaint themes and drafting executive briefings from validated metrics.
- **Where AI Wasted Time / Was Discarded:** Initial attempt to let LLMs calculate timestamp differences or determine breaches produced hallucinatory math. We discarded LLM math entirely in favor of deterministic Pandas logic.

---

### 9. Three-minute recording link.
`https://drive.google.com/file/d/example_vireo_sla_demo/view` *(Placeholder link for submission)*

---

### 10. Three things a Monday handoff owner needs to know.
1. Run `python validate.py` on any new ticket export to verify data integrity before opening the app.
2. Launch the dashboard using `streamlit run app.py`.
3. Never use raw agent volume metrics to penalize Morning shift agents without filtering out overnight creation carryover.

---

### 11. Honest hours spent.
- Data Analysis & Math Verification: **1.5 Hours**
- SLA Engine & Roster Matching Code: **1.5 Hours**
- Streamlit Web Dashboard & UI Aesthetics: **1.0 Hour**
- AI Narrative Module & Documentation: **1.0 Hour**
- **Total Time:** **5.0 Hours**

---

### 12. Public GitHub repository link.
`https://github.com/vireo-support/sla-breach-analyst` *(Placeholder link for submission)*
