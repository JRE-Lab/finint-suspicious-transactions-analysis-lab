diff --git a/scripts/run_lab.py b/scripts/run_lab.py
new file mode 100644
index 0000000000000000000000000000000000000000..95f6e723ea66d245f3f7cc39a99bba9f34e4056d
--- /dev/null
+++ b/scripts/run_lab.py
@@ -0,0 +1,19 @@
+from pathlib import Path
+import sys
+
+ROOT = Path(__file__).resolve().parents[1]
+sys.path.append(str(ROOT / "src"))
+
+from finint_lab.cli import run_lab
+
+
+DATA_PATH = Path("data/synthetic_transactions.csv")
+OUTPUT_DIR = Path("outputs")
+
+
+def main() -> None:
+    run_lab(DATA_PATH, OUTPUT_DIR, seed=7, rows=500, force=False)
+
+
+if __name__ == "__main__":
+    main()
