"""Generate KPI summary tables for management reporting."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORT_DIR = PROJECT_ROOT / "dashboards" / "outputs"


def format_aed(value: float) -> str:
    return f"AED {value:,.0f}"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    monthly = pd.read_csv(DATA_DIR / "monthly_summary.csv")
    category = pd.read_csv(PROCESSED_DIR / "category_summary.csv")
    customers = pd.read_csv(PROCESSED_DIR / "customer_activity.csv")

    totals = {
        "Total Revenue": monthly["revenue_aed"].sum(),
        "Total Expenses": monthly["expenses_aed"].sum(),
        "Net Profit": monthly["net_profit_aed"].sum(),
        "Average Monthly Revenue": monthly["revenue_aed"].mean(),
        "Average Profit Margin %": monthly["profit_margin_pct"].mean(),
        "Average Collection Rate %": monthly["collection_rate_pct"].mean(),
    }

    kpi_summary = pd.DataFrame(
        [
            {"metric": metric, "value": round(value, 1) if " %" in metric else round(value, 0)}
            for metric, value in totals.items()
        ]
    )

    target_tracking = monthly[
        [
            "month",
            "revenue_aed",
            "revenue_target_aed",
            "revenue_vs_target_pct",
            "expenses_aed",
            "expense_budget_aed",
            "expense_budget_used_pct",
            "net_profit_aed",
            "net_profit_target_aed",
            "collection_rate_pct",
            "collection_rate_target_pct",
        ]
    ].copy()

    top_customers = customers.sort_values("revenue_aed", ascending=False).head(8)
    top_expenses = category[category["transaction_type"] == "Expense"].head(8)

    kpi_summary.to_csv(REPORT_DIR / "kpi_summary.csv", index=False)
    target_tracking.to_csv(REPORT_DIR / "kpi_target_tracking.csv", index=False)
    top_customers.to_csv(REPORT_DIR / "top_customers.csv", index=False)
    top_expenses.to_csv(REPORT_DIR / "top_expense_categories.csv", index=False)

    markdown = [
        "# Monthly Management KPI Report",
        "",
        "## Executive KPIs",
        "",
    ]
    for metric, value in totals.items():
        display_value = f"{value:.1f}%" if "%" in metric else format_aed(value)
        markdown.append(f"- **{metric}:** {display_value}")
    markdown.extend(
        [
            "",
            "## Latest Month Snapshot",
            "",
        ]
    )
    latest = monthly.sort_values("month").iloc[-1]
    markdown.extend(
        [
            f"- **Month:** {latest['month']}",
            f"- **Revenue:** {format_aed(latest['revenue_aed'])}",
            f"- **Expenses:** {format_aed(latest['expenses_aed'])}",
            f"- **Net Profit:** {format_aed(latest['net_profit_aed'])}",
            f"- **Profit Margin:** {latest['profit_margin_pct']:.1f}%",
            f"- **Collection Rate:** {latest['collection_rate_pct']:.1f}%",
            "",
            "## Management Notes",
            "",
            "- Revenue is compared against realistic monthly SME targets.",
            "- Expense budget tracking highlights overspend risk by month.",
            "- Customer activity helps identify high-value accounts and collection follow-up needs.",
            "- Data is synthetic and anonymized for portfolio demonstration.",
        ]
    )
    (REPORT_DIR / "management_kpi_report.md").write_text("\n".join(markdown), encoding="utf-8")

    print(f"KPI report files saved in {REPORT_DIR}")


if __name__ == "__main__":
    main()
