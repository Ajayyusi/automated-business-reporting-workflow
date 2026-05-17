-- Monthly reporting queries for management review packs.

-- Monthly P&L view
SELECT
    month,
    revenue_aed,
    expenses_aed,
    net_profit_aed,
    profit_margin_pct
FROM monthly_summary
ORDER BY month;

-- Revenue collection status by month
SELECT
    strftime('%Y-%m', date) AS month,
    collection_status,
    SUM(amount_aed) AS revenue_aed,
    COUNT(*) AS invoice_count
FROM income
GROUP BY strftime('%Y-%m', date), collection_status
ORDER BY month, collection_status;

-- Monthly source-channel quality check
SELECT
    strftime('%Y-%m', date) AS month,
    source_channel,
    transaction_type,
    COUNT(*) AS records_received,
    SUM(amount_aed) AS total_amount_aed
FROM transactions
GROUP BY strftime('%Y-%m', date), source_channel, transaction_type
ORDER BY month, source_channel, transaction_type;

-- Top customers for latest reporting year
SELECT
    customer_name,
    COUNT(*) AS invoice_count,
    SUM(amount_aed) AS revenue_aed,
    SUM(CASE WHEN collection_status = 'Collected' THEN amount_aed ELSE 0 END) AS collected_revenue_aed,
    ROUND(SUM(CASE WHEN collection_status = 'Collected' THEN amount_aed ELSE 0 END) * 100.0 / SUM(amount_aed), 1) AS collection_rate_pct
FROM income
GROUP BY customer_name
ORDER BY revenue_aed DESC
LIMIT 10;

-- Expense approval follow-up
SELECT
    approval_status,
    expense_category,
    COUNT(*) AS expense_count,
    SUM(amount_aed) AS amount_aed
FROM expenses
GROUP BY approval_status, expense_category
ORDER BY approval_status, amount_aed DESC;

-- Months requiring management attention
SELECT
    month,
    revenue_vs_target_pct,
    expense_budget_used_pct,
    collection_rate_pct,
    CASE
        WHEN revenue_vs_target_pct < 90 THEN 'Revenue below target'
        WHEN expense_budget_used_pct > 105 THEN 'Expense overspend'
        WHEN collection_rate_pct < collection_rate_target_pct THEN 'Collections below target'
        ELSE 'On track'
    END AS management_note
FROM monthly_summary
WHERE revenue_vs_target_pct < 90
   OR expense_budget_used_pct > 105
   OR collection_rate_pct < collection_rate_target_pct
ORDER BY month;
