

 # Suspicious Transactions Analysis FININT Lab
 
 This lab teaches you how to conduct financial intelligence (FININT) analysis. FININT involves gathering and analysing information about financial transactions to identify tax evasion, money laundering or financing of criminal and terrorist organisations.
 
 You will:
 - Import a synthetic financial transactions dataset with fields such as amount, sender, receiver, time and jurisdiction.
 - Apply rule-based detection logic to flag structuring (smurfing), round-tripping and flows to high-risk jurisdictions.
 - Build transaction graphs to visualise money flows and identify hubs and cycles.
 - Cross-reference counterparties with public sanctions lists or high-risk entity databases.
 - Rank alerts by risk score and document evidence.
 - Write a FININT report summarising flagged transactions, analysis and recommended actions.
 
 All data in this lab is synthetic or comes from publicly available sources. No sensitive or classified financial information is used.
+
+## Quick start
+
+```bash
+python -m venv .venv
+source .venv/bin/activate
+pip install -r requirements.txt
+pip install -e .
+finint-lab
+```
+
+Outputs are saved to the `outputs/` directory:
+- `alerts.csv` — ranked alert list
+- `report.md` — analyst-style FININT report
+- `transaction_graph.png` — network visualisation of flows
+
+## Lab workflow
+
+1. **Generate data**
+   - `data/synthetic_transactions.csv` is created by `finint_lab.generate_data` if it does not exist.
+2. **Analyze transactions**
+   - `finint_lab.analyze` flags structuring, high-risk jurisdictions, and round-tripping cycles.
+3. **Review outputs**
+   - Inspect the CSV, report, and graph to practice triage and narrative-building.
+
+## CLI options
+
+```bash
+finint-lab --input data/synthetic_transactions.csv --output outputs --seed 7 --rows 500
+```
+
+Use `--force-generate` to regenerate the synthetic dataset even if it already exists.
+
+## Customization ideas
+
+- Update `HIGH_RISK_JURISDICTIONS` in `src/finint_lab/analyze.py` to match a current watch list.
+- Add new rules (e.g., rapid movement through newly created entities).
+- Export the report to PDF using your preferred Markdown toolchain.
