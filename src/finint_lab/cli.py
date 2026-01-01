diff --git a/src/finint_lab/cli.py b/src/finint_lab/cli.py
new file mode 100644
index 0000000000000000000000000000000000000000..417896f395faa474615b8e2dea7728b266ef0564
--- /dev/null
+++ b/src/finint_lab/cli.py
@@ -0,0 +1,79 @@
+from __future__ import annotations
+
+import argparse
+from pathlib import Path
+
+from finint_lab.analyze import analyze_transactions, write_alerts_csv
+from finint_lab.generate_data import generate_synthetic_transactions
+from finint_lab.report import write_report
+
+
+DEFAULT_DATA_PATH = Path("data/synthetic_transactions.csv")
+DEFAULT_OUTPUT_DIR = Path("outputs")
+
+
+def build_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(
+        description="Run the FININT suspicious transactions analysis lab."
+    )
+    parser.add_argument(
+        "--input",
+        type=Path,
+        default=DEFAULT_DATA_PATH,
+        help="Path to the transactions CSV.",
+    )
+    parser.add_argument(
+        "--output",
+        type=Path,
+        default=DEFAULT_OUTPUT_DIR,
+        help="Directory for alerts, report, and graph outputs.",
+    )
+    parser.add_argument(
+        "--seed",
+        type=int,
+        default=7,
+        help="Random seed for synthetic data generation.",
+    )
+    parser.add_argument(
+        "--rows",
+        type=int,
+        default=500,
+        help="Number of synthetic transactions to generate.",
+    )
+    parser.add_argument(
+        "--force-generate",
+        action="store_true",
+        help="Regenerate synthetic data even if the input file exists.",
+    )
+    return parser
+
+
+def run_lab(input_path: Path, output_dir: Path, seed: int, rows: int, force: bool) -> None:
+    if force or not input_path.exists():
+        input_path.parent.mkdir(parents=True, exist_ok=True)
+        generate_synthetic_transactions(input_path, seed=seed, rows=rows)
+
+    results = analyze_transactions(input_path, output_dir)
+    alerts_path = write_alerts_csv(results.alerts, output_dir / "alerts.csv")
+    report_path = write_report(input_path.name, results, output_dir / "report.md")
+
+    print("FININT lab completed.")
+    print(f"- Alerts saved to: {alerts_path}")
+    print(f"- Report saved to: {report_path}")
+    print(f"- Graph saved to: {results.graph_path}")
+
+
+def main() -> None:
+    parser = build_parser()
+    args = parser.parse_args()
+    run_lab(
+        input_path=args.input,
+        output_dir=args.output,
+        seed=args.seed,
+        rows=args.rows,
+        force=args.force_generate,
+    )
+
+
+if __name__ == "__main__":
+    main()
