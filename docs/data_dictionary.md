# Data Dictionary

## customers.csv

| Column | Description |
| --- | --- |
| customer_id | Unique customer identifier |
| customer_name | Synthetic UAE SME customer name |
| sector | Customer industry sector |
| emirate | Customer location |
| relationship_type | Retainer or project-based relationship |
| signup_date | Customer signup date |
| account_manager | Assigned account manager |
| status | Account status |

## income.csv

| Column | Description |
| --- | --- |
| income_id | Unique income record |
| date | Invoice or income date |
| customer_id | Linked customer ID |
| income_category | Revenue category |
| amount_aed | Revenue excluding VAT |
| vat_aed | 5% VAT where applicable |
| total_aed | Revenue including VAT |
| payment_method | Bank transfer, card, cash, or cheque |
| collection_status | Collected or pending |
| source_channel | Simulated data source |

## expenses.csv

| Column | Description |
| --- | --- |
| expense_id | Unique expense record |
| date | Expense date |
| vendor | Synthetic vendor name |
| expense_category | Spend category |
| amount_aed | Expense excluding VAT |
| vat_aed | VAT where applicable |
| payment_method | Bank transfer, card, cash, or cheque |
| approval_status | Approved or pending review |
| source_channel | Simulated data source |

## monthly_summary.csv

| Column | Description |
| --- | --- |
| revenue_aed | Monthly revenue |
| expenses_aed | Monthly expenses |
| net_profit_aed | Revenue minus expenses |
| profit_margin_pct | Net profit divided by revenue |
| collection_rate_pct | Collected revenue divided by total revenue |
| revenue_vs_target_pct | Revenue actual compared with target |
| expense_budget_used_pct | Expenses actual compared with budget |
