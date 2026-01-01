diff --git a/src/finint_lab/__init__.py b/src/finint_lab/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..52ae0c0584c9445c02c9fcd86a40fab35febf71b
--- /dev/null
+++ b/src/finint_lab/__init__.py
@@ -0,0 +1,7 @@
+"""FININT suspicious transactions analysis lab."""
+
+from finint_lab.analyze import analyze_transactions
+from finint_lab.generate_data import generate_synthetic_transactions
+from finint_lab.report import write_report
+
+__all__ = ["generate_synthetic_transactions", "analyze_transactions", "write_report"]
