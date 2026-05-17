-- Useful KPI queries for SME business reporting.

-- 1. Monthly revenue
SELECT
    strftime('%Y-%m', date) AS month,
    SUM(amount_aed) AS revenue_aed,
    COUNT(*) AS invoice_count
FROM income
GROUP BY strftime('%Y-%m', date)
ORDER BY month;

-- 2. Monthly expenses
SELECT
    strftime('%Y-%m', date) AS month,
    SUM(amount_aed) AS expenses_aed,
    COUNT(*) AS expense_count
FROM expenses
GROUP BY strftime('%Y-%m', date)
ORDER BY month;

-- 3. Net profit by month
SELECT
    m.month,
    m.revenue_aed,
    m.expenses_aed,
    m.net_profit_aed,
    m.profit_margin_pct
FROM monthly_summary m
ORDER BY m.month;

-- 4. Expense category breakdown
SELECT
    expense_category,
    SUM(amount_aed) AS total_expense_aed,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_aed) * 100.0 / (SELECT SUM(amount_aed) FROM expenses), 1) AS share_of_expenses_pct
FROM expenses
GROUP BY expense_category
ORDER BY total_expense_aed DESC;

-- 5. Customer activity and revenue contribution
SELECT
    c.customer_id,
    c.customer_name,
    c.sector,
    c.emirate,
    COUNT(i.income_id) AS invoice_count,
    COALESCE(SUM(i.amount_aed), 0) AS revenue_aed,
    MAX(i.date) AS last_invoice_date
FROM customers c
LEFT JOIN income i ON c.customer_id = i.customer_id
GROUP BY c.customer_id, c.customer_name, c.sector, c.emirate
ORDER BY revenue_aed DESC;

-- 6. Cash vs bank/digital transactions
SELECT
    CASE WHEN payment_method = 'Cash' THEN 'Cash' ELSE 'Bank / Digital' END AS payment_group,
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount_aed) AS total_amount_aed
FROM transactions
GROUP BY
    CASE WHEN payment_method = 'Cash' THEN 'Cash' ELSE 'Bank / Digital' END,
    transaction_type
ORDER BY payment_group, transaction_type;

-- 7. KPI target vs actual performance
SELECT
    month,
    revenue_aed,
    revenue_target_aed,
    revenue_vs_target_pct,
    expenses_aed,
    expense_budget_aed,
    expense_budget_used_pct,
    net_profit_aed,
    net_profit_target_aed,
    collection_rate_pct,
    collection_rate_target_pct
FROM monthly_summary
ORDER BY month;
