diff --git a/src/finint_lab/generate_data.py b/src/finint_lab/generate_data.py
new file mode 100644
index 0000000000000000000000000000000000000000..00af778a1c92ee6e9196e74b63a077a06e322fa0
--- /dev/null
+++ b/src/finint_lab/generate_data.py
@@ -0,0 +1,123 @@
+import random
+from datetime import datetime, timedelta
+from pathlib import Path
+
+import numpy as np
+import pandas as pd
+
+CURRENCIES = ["USD", "EUR", "GBP"]
+JURISDICTIONS = ["US", "GB", "DE", "NL", "AE", "RU", "IR", "CN", "SG"]
+HIGH_RISK_JURISDICTIONS = {"RU", "IR"}
+DESCRIPTIONS = [
+    "Consulting fee",
+    "Invoice payment",
+    "Logistics services",
+    "Software license",
+    "Marketing support",
+    "Trade settlement",
+    "Equipment purchase",
+]
+
+
+
+def _random_entity(prefix: str, idx: int) -> str:
+    return f"{prefix}{idx:03d}"
+
+
+def generate_synthetic_transactions(
+    output_path: Path,
+    seed: int = 7,
+    rows: int = 500,
+) -> pd.DataFrame:
+    random.seed(seed)
+    np.random.seed(seed)
+
+    base_time = datetime.utcnow() - timedelta(days=30)
+
+    senders = [_random_entity("S", i) for i in range(1, 41)]
+    receivers = [_random_entity("R", i) for i in range(1, 41)]
+
+    data = []
+    for idx in range(1, rows + 1):
+        sender = random.choice(senders)
+        receiver = random.choice(receivers)
+        timestamp = base_time + timedelta(hours=random.randint(0, 720))
+        amount = round(abs(np.random.normal(4500, 2200)) + 50, 2)
+        currency = random.choice(CURRENCIES)
+        sender_jurisdiction = random.choice(JURISDICTIONS)
+        receiver_jurisdiction = random.choice(JURISDICTIONS)
+        description = random.choice(DESCRIPTIONS)
+        data.append(
+            {
+                "transaction_id": f"T{idx:05d}",
+                "timestamp": timestamp.isoformat(timespec="minutes"),
+                "amount": amount,
+                "currency": currency,
+                "sender_id": sender,
+                "receiver_id": receiver,
+                "sender_jurisdiction": sender_jurisdiction,
+                "receiver_jurisdiction": receiver_jurisdiction,
+                "description": description,
+            }
+        )
+
+    df = pd.DataFrame(data)
+
+    # Inject structuring pattern
+    for i in range(5):
+        df.loc[len(df)] = {
+            "transaction_id": f"TSMURF{i+1:03d}",
+            "timestamp": (base_time + timedelta(days=2, hours=i)).isoformat(
+                timespec="minutes"
+            ),
+            "amount": 9800.00,
+            "currency": "USD",
+            "sender_id": "S999",
+            "receiver_id": "R888",
+            "sender_jurisdiction": "US",
+            "receiver_jurisdiction": "US",
+            "description": "Cash deposit",
+        }
+
+    # Inject round-tripping cycle
+    cycle_entities = ["S777", "S778", "S779"]
+    for i in range(3):
+        df.loc[len(df)] = {
+            "transaction_id": f"TRIP{i+1:03d}",
+            "timestamp": (base_time + timedelta(days=5, hours=i)).isoformat(
+                timespec="minutes"
+            ),
+            "amount": 25000.00,
+            "currency": "USD",
+            "sender_id": cycle_entities[i],
+            "receiver_id": cycle_entities[(i + 1) % 3],
+            "sender_jurisdiction": "US",
+            "receiver_jurisdiction": "NL",
+            "description": "Intercompany transfer",
+        }
+
+    # Inject high-risk jurisdiction flows
+    for i in range(3):
+        df.loc[len(df)] = {
+            "transaction_id": f"HRISK{i+1:03d}",
+            "timestamp": (base_time + timedelta(days=7, hours=i)).isoformat(
+                timespec="minutes"
+            ),
+            "amount": 12000.00,
+            "currency": "EUR",
+            "sender_id": "S555",
+            "receiver_id": "R555",
+            "sender_jurisdiction": "DE",
+            "receiver_jurisdiction": random.choice(tuple(HIGH_RISK_JURISDICTIONS)),
+            "description": "International transfer",
+        }
+
+    df.to_csv(output_path, index=False)
+    return df
+
+
+if __name__ == "__main__":
+    output = Path("data/synthetic_transactions.csv")
+    output.parent.mkdir(parents=True, exist_ok=True)
+    generate_synthetic_transactions(output)
+    print(f"Synthetic transactions saved to {output}")
