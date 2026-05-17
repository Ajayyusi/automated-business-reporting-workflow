"""Generate realistic sample data for a UAE SME service business.

The data represents a small facilities and office support services company.
It is synthetic but shaped to look like the kind of operational reporting
data a junior BI analyst might automate for management review.
"""

from __future__ import annotations

from pathlib import Path
import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


CUSTOMERS = [
    ("CUST-001", "Desert Pearl Clinics", "Healthcare", "Dubai", "Retainer"),
    ("CUST-002", "Al Noor Business Center", "Business Services", "Abu Dhabi", "Project"),
    ("CUST-003", "Palm View Real Estate", "Real Estate", "Dubai", "Retainer"),
    ("CUST-004", "Gulf Star Trading", "Trading", "Sharjah", "Project"),
    ("CUST-005", "Marina Fit Studio", "Fitness", "Dubai", "Retainer"),
    ("CUST-006", "Blue Dhow Logistics", "Logistics", "Jebel Ali", "Retainer"),
    ("CUST-007", "Ajman Modern School", "Education", "Ajman", "Project"),
    ("CUST-008", "Falcon Legal Advisors", "Professional Services", "Dubai", "Retainer"),
    ("CUST-009", "Oasis Cafe Group", "Hospitality", "Dubai", "Project"),
    ("CUST-010", "Capital Dental Center", "Healthcare", "Abu Dhabi", "Retainer"),
    ("CUST-011", "Ras Al Khaimah Warehousing", "Logistics", "RAK", "Project"),
    ("CUST-012", "Mirdif Learning Hub", "Education", "Dubai", "Retainer"),
]

INCOME_CATEGORIES = [
    ("Monthly service retainer", 0.45, 8500, 22000),
    ("Automation setup fee", 0.16, 6000, 18500),
    ("Dashboard customization", 0.15, 3500, 12000),
    ("Data cleaning support", 0.12, 2500, 9000),
    ("Training workshop", 0.07, 1800, 6500),
    ("Ad hoc reporting", 0.05, 1200, 5000),
]

EXPENSE_CATEGORIES = [
    ("Salaries and wages", 0.25, 18000, 32000),
    ("Software subscriptions", 0.14, 900, 3800),
    ("Office rent", 0.12, 7500, 12500),
    ("Marketing", 0.11, 1200, 6500),
    ("Transport and fuel", 0.10, 800, 4200),
    ("Telecom and internet", 0.08, 600, 2200),
    ("Professional fees", 0.07, 1000, 5000),
    ("Office supplies", 0.06, 300, 1800),
    ("Bank charges", 0.04, 80, 450),
    ("Maintenance", 0.03, 500, 2500),
]

PAYMENT_METHODS = ["Bank Transfer", "Card", "Cash", "Cheque"]
CHANNELS = ["Telegram Form", "Manual Entry", "Google Sheet Import", "Accounting Export"]


def weighted_choice(options: list[tuple[str, float, int, int]]) -> tuple[str, int, int]:
    labels = [item[0] for item in options]
    weights = [item[1] for item in options]
    selected = random.choices(labels, weights=weights, k=1)[0]
    for label, _, low, high in options:
        if label == selected:
            return label, low, high
    raise RuntimeError("Invalid weighted choice")


def random_business_day(month_start: pd.Timestamp) -> pd.Timestamp:
    month_end = month_start + pd.offsets.MonthEnd(0)
    days = pd.bdate_range(month_start, month_end)
    return random.choice(list(days))


def build_customers() -> pd.DataFrame:
    rows = []
    for customer_id, name, sector, emirate, relationship in CUSTOMERS:
        signup = pd.Timestamp("2023-01-01") + pd.Timedelta(days=random.randint(0, 520))
        rows.append(
            {
                "customer_id": customer_id,
                "customer_name": name,
                "sector": sector,
                "emirate": emirate,
                "relationship_type": relationship,
                "signup_date": signup.date().isoformat(),
                "account_manager": random.choice(["Aisha", "Omar", "Nadia", "Khalid"]),
                "status": random.choices(["Active", "Active", "Active", "At Risk"], [0.42, 0.32, 0.18, 0.08])[0],
            }
        )
    return pd.DataFrame(rows)


def build_income(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    invoice_no = 1001
    for month in pd.date_range("2025-01-01", "2025-12-01", freq="MS"):
        active_customers = customers.sample(n=random.randint(7, 11), random_state=random.randint(1, 9999))
        for _, customer in active_customers.iterrows():
            category, low, high = weighted_choice(INCOME_CATEGORIES)
            amount = round(random.uniform(low, high) / 50) * 50
            vat = round(amount * 0.05, 2)
            date = random_business_day(month)
            rows.append(
                {
                    "income_id": f"INC-{invoice_no}",
                    "date": date.date().isoformat(),
                    "customer_id": customer["customer_id"],
                    "customer_name": customer["customer_name"],
                    "income_category": category,
                    "description": f"{category} - {customer['customer_name']}",
                    "amount_aed": amount,
                    "vat_aed": vat,
                    "total_aed": round(amount + vat, 2),
                    "payment_method": random.choices(PAYMENT_METHODS, [0.70, 0.12, 0.08, 0.10])[0],
                    "collection_status": random.choices(["Collected", "Collected", "Pending"], [0.62, 0.25, 0.13])[0],
                    "source_channel": random.choices(CHANNELS, [0.25, 0.22, 0.35, 0.18])[0],
                }
            )
            invoice_no += 1
    return pd.DataFrame(rows)


def build_expenses() -> pd.DataFrame:
    rows = []
    expense_no = 5001
    vendors = {
        "Salaries and wages": "Internal Payroll",
        "Software subscriptions": "Cloud Software Vendor",
        "Office rent": "Business Bay Properties",
        "Marketing": "UAE Digital Ads",
        "Transport and fuel": "Fleet Fuel Card",
        "Telecom and internet": "Etisalat",
        "Professional fees": "Local Accounting Office",
        "Office supplies": "Stationery Market LLC",
        "Bank charges": "Bank Service Fees",
        "Maintenance": "Office Maintenance Co.",
    }
    fixed_expenses = [
        ("Salaries and wages", 26000, 34500),
        ("Office rent", 8500, 11500),
        ("Software subscriptions", 1800, 4200),
        ("Telecom and internet", 850, 1800),
    ]
    variable_categories = [
        ("Marketing", 0.22, 900, 5200),
        ("Transport and fuel", 0.22, 650, 3200),
        ("Professional fees", 0.15, 850, 4200),
        ("Office supplies", 0.15, 250, 1400),
        ("Bank charges", 0.14, 60, 360),
        ("Maintenance", 0.12, 450, 2200),
    ]
    for month in pd.date_range("2025-01-01", "2025-12-01", freq="MS"):
        monthly_rows = list(fixed_expenses)
        monthly_rows.extend(weighted_choice(variable_categories) for _ in range(random.randint(9, 15)))
        for category, low, high in monthly_rows:
            amount = round(random.uniform(low, high) / 25) * 25
            rows.append(
                {
                    "expense_id": f"EXP-{expense_no}",
                    "date": random_business_day(month).date().isoformat(),
                    "vendor": vendors[category],
                    "expense_category": category,
                    "description": f"{category} expense",
                    "amount_aed": amount,
                    "vat_aed": round(amount * 0.05, 2) if category not in ["Salaries and wages", "Bank charges"] else 0,
                    "payment_method": random.choices(PAYMENT_METHODS, [0.64, 0.18, 0.13, 0.05])[0],
                    "approval_status": random.choices(["Approved", "Approved", "Pending Review"], [0.72, 0.18, 0.10])[0],
                    "source_channel": random.choices(CHANNELS, [0.20, 0.30, 0.22, 0.28])[0],
                }
            )
            expense_no += 1
    return pd.DataFrame(rows)


def build_transactions(income: pd.DataFrame, expenses: pd.DataFrame) -> pd.DataFrame:
    income_tx = income.rename(columns={"income_id": "source_id", "income_category": "category"}).copy()
    income_tx["transaction_type"] = "Income"
    income_tx["signed_amount_aed"] = income_tx["amount_aed"]
    income_tx = income_tx[
        ["source_id", "date", "transaction_type", "category", "description", "amount_aed", "signed_amount_aed", "payment_method", "source_channel"]
    ]

    expense_tx = expenses.rename(columns={"expense_id": "source_id", "expense_category": "category"}).copy()
    expense_tx["transaction_type"] = "Expense"
    expense_tx["signed_amount_aed"] = -expense_tx["amount_aed"]
    expense_tx = expense_tx[
        ["source_id", "date", "transaction_type", "category", "description", "amount_aed", "signed_amount_aed", "payment_method", "source_channel"]
    ]

    transactions = pd.concat([income_tx, expense_tx], ignore_index=True)
    transactions.insert(0, "transaction_id", [f"TRX-{i:05d}" for i in range(1, len(transactions) + 1)])
    return transactions.sort_values("date").reset_index(drop=True)


def build_kpi_targets() -> pd.DataFrame:
    rows = []
    for month in pd.date_range("2025-01-01", "2025-12-01", freq="MS"):
        seasonality = 1.12 if month.month in [3, 4, 10, 11] else 0.92 if month.month in [7, 8] else 1.0
        rows.append(
            {
                "month": month.strftime("%Y-%m"),
                "revenue_target_aed": round(125000 * seasonality / 1000) * 1000,
                "expense_budget_aed": round(82000 * seasonality / 1000) * 1000,
                "net_profit_target_aed": round(38000 * seasonality / 1000) * 1000,
                "collection_rate_target_pct": 92,
                "active_customers_target": 9,
            }
        )
    return pd.DataFrame(rows)


def build_monthly_summary(income: pd.DataFrame, expenses: pd.DataFrame, kpi_targets: pd.DataFrame) -> pd.DataFrame:
    income_m = income.assign(month=pd.to_datetime(income["date"]).dt.strftime("%Y-%m"))
    expense_m = expenses.assign(month=pd.to_datetime(expenses["date"]).dt.strftime("%Y-%m"))

    revenue = income_m.groupby("month", as_index=False).agg(
        revenue_aed=("amount_aed", "sum"),
        collected_revenue_aed=("amount_aed", lambda s: income_m.loc[s.index][income_m.loc[s.index, "collection_status"] == "Collected"]["amount_aed"].sum()),
        active_customers=("customer_id", "nunique"),
        invoice_count=("income_id", "count"),
    )
    exp = expense_m.groupby("month", as_index=False).agg(
        expenses_aed=("amount_aed", "sum"),
        expense_count=("expense_id", "count"),
    )
    summary = revenue.merge(exp, on="month", how="outer").fillna(0)
    summary["net_profit_aed"] = summary["revenue_aed"] - summary["expenses_aed"]
    summary["profit_margin_pct"] = (summary["net_profit_aed"] / summary["revenue_aed"] * 100).round(1)
    summary["collection_rate_pct"] = (summary["collected_revenue_aed"] / summary["revenue_aed"] * 100).round(1)
    summary = summary.merge(kpi_targets, on="month", how="left")
    summary["revenue_vs_target_pct"] = (summary["revenue_aed"] / summary["revenue_target_aed"] * 100).round(1)
    summary["expense_budget_used_pct"] = (summary["expenses_aed"] / summary["expense_budget_aed"] * 100).round(1)
    return summary.sort_values("month")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    customers = build_customers()
    income = build_income(customers)
    expenses = build_expenses()
    transactions = build_transactions(income, expenses)
    kpi_targets = build_kpi_targets()
    monthly_summary = build_monthly_summary(income, expenses, kpi_targets)

    customers.to_csv(DATA_DIR / "customers.csv", index=False)
    income.to_csv(DATA_DIR / "income.csv", index=False)
    expenses.to_csv(DATA_DIR / "expenses.csv", index=False)
    transactions.to_csv(DATA_DIR / "transactions.csv", index=False)
    kpi_targets.to_csv(DATA_DIR / "kpi_targets.csv", index=False)
    monthly_summary.to_csv(DATA_DIR / "monthly_summary.csv", index=False)

    print(f"Generated sample data in {DATA_DIR}")
    print(f"Transactions: {len(transactions):,} | Income records: {len(income):,} | Expense records: {len(expenses):,}")


if __name__ == "__main__":
    main()
