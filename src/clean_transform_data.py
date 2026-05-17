"""Clean and transform source CSV files for reporting outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def prepare_transactions() -> pd.DataFrame:
    transactions = load_csv("transactions.csv")
    transactions.columns = [col.strip().lower() for col in transactions.columns]

    transactions["date"] = pd.to_datetime(transactions["date"], errors="coerce")
    for col in ["transaction_type", "category", "description", "payment_method", "source_channel"]:
        transactions[col] = transactions[col].map(normalize_text)

    numeric_cols = ["amount_aed", "signed_amount_aed"]
    for col in numeric_cols:
        transactions[col] = pd.to_numeric(transactions[col], errors="coerce").fillna(0)

    transactions = transactions.dropna(subset=["date"])
    transactions["month"] = transactions["date"].dt.strftime("%Y-%m")
    transactions["quarter"] = transactions["date"].dt.to_period("Q").astype(str)
    transactions["cash_or_bank"] = transactions["payment_method"].map(
        lambda method: "Cash" if method == "Cash" else "Bank / Digital"
    )
    transactions["is_income"] = transactions["transaction_type"].eq("Income")
    transactions["is_expense"] = transactions["transaction_type"].eq("Expense")

    return transactions.sort_values(["date", "transaction_id"]).reset_index(drop=True)


def prepare_customer_activity(income: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    income["date"] = pd.to_datetime(income["date"], errors="coerce")
    income["amount_aed"] = pd.to_numeric(income["amount_aed"], errors="coerce").fillna(0)
    activity = income.groupby("customer_id", as_index=False).agg(
        revenue_aed=("amount_aed", "sum"),
        invoice_count=("income_id", "count"),
        last_invoice_date=("date", "max"),
        collected_revenue_aed=("amount_aed", lambda s: income.loc[s.index][income.loc[s.index, "collection_status"] == "Collected"]["amount_aed"].sum()),
    )
    activity["collection_rate_pct"] = (activity["collected_revenue_aed"] / activity["revenue_aed"] * 100).round(1)
    return customers.merge(activity, on="customer_id", how="left").fillna(
        {"revenue_aed": 0, "invoice_count": 0, "collected_revenue_aed": 0, "collection_rate_pct": 0}
    )


def build_category_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    return (
        transactions.groupby(["transaction_type", "category"], as_index=False)
        .agg(total_aed=("amount_aed", "sum"), transaction_count=("transaction_id", "count"))
        .sort_values(["transaction_type", "total_aed"], ascending=[True, False])
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    transactions = prepare_transactions()
    income = load_csv("income.csv")
    customers = load_csv("customers.csv")

    customer_activity = prepare_customer_activity(income, customers)
    category_summary = build_category_summary(transactions)

    transactions.to_csv(OUTPUT_DIR / "clean_transactions.csv", index=False)
    customer_activity.to_csv(OUTPUT_DIR / "customer_activity.csv", index=False)
    category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)

    print(f"Cleaned data saved in {OUTPUT_DIR}")
    print(f"Clean transactions: {len(transactions):,} | Customer records: {len(customer_activity):,}")


if __name__ == "__main__":
    main()
