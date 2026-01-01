diff --git a/src/finint_lab/analyze.py b/src/finint_lab/analyze.py
new file mode 100644
index 0000000000000000000000000000000000000000..6406b52187ed30c59605f0d599e59b8dd344125e
--- /dev/null
+++ b/src/finint_lab/analyze.py
@@ -0,0 +1,170 @@
+from __future__ import annotations
+
+from collections import defaultdict
+from dataclasses import dataclass
+from pathlib import Path
+
+import matplotlib
+
+matplotlib.use("Agg")
+
+import matplotlib.pyplot as plt
+import networkx as nx
+import pandas as pd
+
+HIGH_RISK_JURISDICTIONS = {"RU", "IR"}
+
+
+@dataclass
+class Alert:
+    alert_id: str
+    alert_type: str
+    risk_score: int
+    description: str
+    related_transactions: list[str]
+
+
+@dataclass
+class AnalysisResults:
+    alerts: list[Alert]
+    graph_path: Path
+
+
+def _detect_structuring(df: pd.DataFrame) -> list[Alert]:
+    alerts = []
+    df = df.copy()
+    df["timestamp"] = pd.to_datetime(df["timestamp"])
+    df["day"] = df["timestamp"].dt.date
+
+    grouped = df.groupby(["sender_id", "receiver_id", "day"])
+    for (sender, receiver, day), group in grouped:
+        if len(group) >= 3 and group["amount"].lt(10000).all() and group["amount"].sum() >= 25000:
+            alerts.append(
+                Alert(
+                    alert_id=f"STRUCT-{sender}-{receiver}-{day}",
+                    alert_type="Structuring",
+                    risk_score=30,
+                    description=(
+                        "Multiple sub-threshold transactions within 24 hours "
+                        f"from {sender} to {receiver}."
+                    ),
+                    related_transactions=group["transaction_id"].tolist(),
+                )
+            )
+    return alerts
+
+
+def _detect_high_risk_jurisdiction(df: pd.DataFrame) -> list[Alert]:
+    alerts = []
+    hits = df[
+        (df["sender_jurisdiction"].isin(HIGH_RISK_JURISDICTIONS))
+        | (df["receiver_jurisdiction"].isin(HIGH_RISK_JURISDICTIONS))
+    ]
+    for _, row in hits.iterrows():
+        alerts.append(
+            Alert(
+                alert_id=f"HRISK-{row['transaction_id']}",
+                alert_type="High-Risk Jurisdiction",
+                risk_score=25,
+                description=(
+                    "Transaction involves a high-risk jurisdiction: "
+                    f"{row['sender_jurisdiction']} -> {row['receiver_jurisdiction']}."
+                ),
+                related_transactions=[row["transaction_id"]],
+            )
+        )
+    return alerts
+
+
+def _detect_round_tripping(df: pd.DataFrame) -> list[Alert]:
+    graph = nx.DiGraph()
+    for _, row in df.iterrows():
+        graph.add_edge(row["sender_id"], row["receiver_id"], transaction_id=row["transaction_id"])
+
+    alerts = []
+    cycles = [cycle for cycle in nx.simple_cycles(graph) if 2 < len(cycle) <= 4]
+    seen = set()
+    for cycle in cycles:
+        cycle_key = tuple(sorted(cycle))
+        if cycle_key in seen:
+            continue
+        seen.add(cycle_key)
+        related_transactions = []
+        for i in range(len(cycle)):
+            sender = cycle[i]
+            receiver = cycle[(i + 1) % len(cycle)]
+            related_transactions.append(graph[sender][receiver]["transaction_id"])
+        alerts.append(
+            Alert(
+                alert_id=f"CYCLE-{'-'.join(cycle)}",
+                alert_type="Round-Tripping",
+                risk_score=40,
+                description=(
+                    "Funds cycle through multiple entities before returning to origin: "
+                    f"{' -> '.join(cycle)}."
+                ),
+                related_transactions=related_transactions,
+            )
+        )
+    return alerts
+
+
+def _build_transaction_graph(df: pd.DataFrame, output_path: Path) -> Path:
+    graph = nx.DiGraph()
+    for _, row in df.iterrows():
+        graph.add_edge(
+            row["sender_id"],
+            row["receiver_id"],
+            weight=row["amount"],
+        )
+
+    plt.figure(figsize=(10, 8))
+    pos = nx.spring_layout(graph, seed=7)
+    weights = [graph[u][v]["weight"] for u, v in graph.edges()]
+    nx.draw_networkx_nodes(graph, pos, node_size=200, node_color="#2c7fb8")
+    nx.draw_networkx_edges(graph, pos, width=[max(w / 8000, 0.5) for w in weights], alpha=0.6)
+    nx.draw_networkx_labels(graph, pos, font_size=6)
+    plt.axis("off")
+    output_path.parent.mkdir(parents=True, exist_ok=True)
+    plt.tight_layout()
+    plt.savefig(output_path, dpi=200)
+    plt.close()
+    return output_path
+
+
+def analyze_transactions(input_path: Path, output_dir: Path) -> AnalysisResults:
+    df = pd.read_csv(input_path)
+    alerts = []
+    alerts.extend(_detect_structuring(df))
+    alerts.extend(_detect_high_risk_jurisdiction(df))
+    alerts.extend(_detect_round_tripping(df))
+
+    graph_path = _build_transaction_graph(df, output_dir / "transaction_graph.png")
+
+    return AnalysisResults(alerts=alerts, graph_path=graph_path)
+
+
+def write_alerts_csv(alerts: list[Alert], output_path: Path) -> Path:
+    rows = []
+    for alert in alerts:
+        rows.append(
+            {
+                "alert_id": alert.alert_id,
+                "alert_type": alert.alert_type,
+                "risk_score": alert.risk_score,
+                "description": alert.description,
+                "related_transactions": ",".join(alert.related_transactions),
+            }
+        )
+    output_path.parent.mkdir(parents=True, exist_ok=True)
+    pd.DataFrame(rows).sort_values("risk_score", ascending=False).to_csv(
+        output_path, index=False
+    )
+    return output_path
+
+
+def summarize_alerts(alerts: list[Alert]) -> dict[str, int]:
+    summary = defaultdict(int)
+    for alert in alerts:
+        summary[alert.alert_type] += 1
+    return dict(summary)
