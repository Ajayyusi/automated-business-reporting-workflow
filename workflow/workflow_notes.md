# Workflow Notes

The reporting workflow is designed to be realistic for an SME service business:

1. Income and expense records are received through simple channels such as Telegram forms, manual entry, Google Sheets, or accounting exports.
2. Python scripts clean dates, categories, amounts, payment methods, and transaction types.
3. Clean data is saved to CSV files that can be loaded into Google Sheets, SQLite, PostgreSQL, Power BI, or Looker Studio.
4. SQL queries provide repeatable reporting logic for revenue, expenses, profit, customer activity, and KPI tracking.
5. Dashboard screenshots summarize the same outputs for management review.

The workflow intentionally avoids heavy frameworks so it stays understandable and believable for a junior BI/data automation portfolio project.
