-- Database schema for the automated business reporting workflow.
-- Designed for SQLite/PostgreSQL-style analytics tables with simple types.

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(120) NOT NULL,
    sector VARCHAR(80),
    emirate VARCHAR(60),
    relationship_type VARCHAR(40),
    signup_date DATE,
    account_manager VARCHAR(80),
    status VARCHAR(40)
);

CREATE TABLE income (
    income_id VARCHAR(20) PRIMARY KEY,
    date DATE NOT NULL,
    customer_id VARCHAR(20),
    customer_name VARCHAR(120),
    income_category VARCHAR(80),
    description VARCHAR(255),
    amount_aed DECIMAL(12, 2),
    vat_aed DECIMAL(12, 2),
    total_aed DECIMAL(12, 2),
    payment_method VARCHAR(40),
    collection_status VARCHAR(40),
    source_channel VARCHAR(80),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE expenses (
    expense_id VARCHAR(20) PRIMARY KEY,
    date DATE NOT NULL,
    vendor VARCHAR(120),
    expense_category VARCHAR(80),
    description VARCHAR(255),
    amount_aed DECIMAL(12, 2),
    vat_aed DECIMAL(12, 2),
    payment_method VARCHAR(40),
    approval_status VARCHAR(40),
    source_channel VARCHAR(80)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    source_id VARCHAR(20),
    date DATE NOT NULL,
    transaction_type VARCHAR(20),
    category VARCHAR(80),
    description VARCHAR(255),
    amount_aed DECIMAL(12, 2),
    signed_amount_aed DECIMAL(12, 2),
    payment_method VARCHAR(40),
    source_channel VARCHAR(80)
);

CREATE TABLE kpi_targets (
    month VARCHAR(7) PRIMARY KEY,
    revenue_target_aed DECIMAL(12, 2),
    expense_budget_aed DECIMAL(12, 2),
    net_profit_target_aed DECIMAL(12, 2),
    collection_rate_target_pct DECIMAL(5, 2),
    active_customers_target INTEGER
);

CREATE TABLE monthly_summary (
    month VARCHAR(7) PRIMARY KEY,
    revenue_aed DECIMAL(12, 2),
    collected_revenue_aed DECIMAL(12, 2),
    active_customers INTEGER,
    invoice_count INTEGER,
    expenses_aed DECIMAL(12, 2),
    expense_count INTEGER,
    net_profit_aed DECIMAL(12, 2),
    profit_margin_pct DECIMAL(5, 2),
    collection_rate_pct DECIMAL(5, 2),
    revenue_target_aed DECIMAL(12, 2),
    expense_budget_aed DECIMAL(12, 2),
    net_profit_target_aed DECIMAL(12, 2),
    collection_rate_target_pct DECIMAL(5, 2),
    active_customers_target INTEGER,
    revenue_vs_target_pct DECIMAL(5, 2),
    expense_budget_used_pct DECIMAL(5, 2)
);
