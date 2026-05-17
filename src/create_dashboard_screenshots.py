"""Create dashboard screenshots and workflow diagram from the reporting data."""

from __future__ import annotations

from pathlib import Path
import os

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
DASHBOARD_DIR = PROJECT_ROOT / "dashboards"
ASSETS_DIR = PROJECT_ROOT / "assets"
MPL_CACHE_DIR = PROJECT_ROOT / ".matplotlib-cache"

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

COLOR_NAVY = "#263238"
COLOR_TEAL = "#00897B"
COLOR_BLUE = "#1976D2"
COLOR_GREEN = "#2E7D32"
COLOR_RED = "#C62828"
COLOR_AMBER = "#F9A825"
COLOR_GREY = "#ECEFF1"
COLOR_TEXT = "#37474F"


def money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"AED {value / 1_000_000:.1f}M"
    return f"AED {value / 1_000:.0f}K"


def style_axis(ax, title: str) -> None:
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=COLOR_NAVY, pad=12)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#CFD8DC", linewidth=0.8, alpha=0.8)
    ax.tick_params(axis="x", rotation=35, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)


def add_kpi_card(fig, x: float, y: float, w: float, h: float, label: str, value: str, accent: str) -> None:
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        transform=fig.transFigure,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1,
        facecolor="white",
        edgecolor="#CFD8DC",
    )
    fig.patches.append(rect)
    fig.text(x + 0.018, y + h - 0.032, label, fontsize=9, color=COLOR_TEXT)
    fig.text(x + 0.018, y + 0.028, value, fontsize=17, fontweight="bold", color=accent)


def save_figure(fig, filename: str) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(DASHBOARD_DIR / filename, dpi=180, bbox_inches="tight", facecolor="#F7F9FA")
    plt.close(fig)


def executive_overview(monthly: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(14, 8), facecolor="#F7F9FA")
    fig.suptitle("Executive Overview | UAE SME Reporting Automation", x=0.06, y=0.96, ha="left", fontsize=18, fontweight="bold", color=COLOR_NAVY)
    fig.text(0.06, 0.925, "Income, expenses, profitability, and collection performance tracked from automated source data.", fontsize=10, color=COLOR_TEXT)

    add_kpi_card(fig, 0.06, 0.78, 0.20, 0.10, "Total Revenue", money(monthly["revenue_aed"].sum()), COLOR_BLUE)
    add_kpi_card(fig, 0.29, 0.78, 0.20, 0.10, "Total Expenses", money(monthly["expenses_aed"].sum()), COLOR_RED)
    add_kpi_card(fig, 0.52, 0.78, 0.20, 0.10, "Net Profit", money(monthly["net_profit_aed"].sum()), COLOR_GREEN)
    add_kpi_card(fig, 0.75, 0.78, 0.18, 0.10, "Avg Collection", f"{monthly['collection_rate_pct'].mean():.1f}%", COLOR_TEAL)

    ax1 = fig.add_axes([0.07, 0.42, 0.55, 0.25])
    ax1.plot(monthly["month"], monthly["revenue_aed"], marker="o", color=COLOR_BLUE, linewidth=2.5, label="Revenue")
    ax1.plot(monthly["month"], monthly["expenses_aed"], marker="o", color=COLOR_RED, linewidth=2.5, label="Expenses")
    ax1.plot(monthly["month"], monthly["net_profit_aed"], marker="o", color=COLOR_GREEN, linewidth=2.5, label="Net Profit")
    style_axis(ax1, "Monthly Performance")
    ax1.legend(frameon=False, fontsize=9, loc="upper left")

    ax2 = fig.add_axes([0.69, 0.42, 0.24, 0.25])
    colors = [COLOR_GREEN if v >= 100 else COLOR_AMBER for v in monthly["revenue_vs_target_pct"]]
    ax2.bar(monthly["month"], monthly["revenue_vs_target_pct"], color=colors)
    ax2.axhline(100, color=COLOR_NAVY, linewidth=1.2, linestyle="--")
    style_axis(ax2, "Revenue Target Achievement %")
    ax2.set_ylim(0, max(130, monthly["revenue_vs_target_pct"].max() + 10))

    ax3 = fig.add_axes([0.07, 0.10, 0.38, 0.22])
    ax3.bar(monthly["month"], monthly["profit_margin_pct"], color=COLOR_TEAL)
    style_axis(ax3, "Profit Margin %")

    ax4 = fig.add_axes([0.55, 0.10, 0.38, 0.22])
    ax4.plot(monthly["month"], monthly["collection_rate_pct"], marker="o", color=COLOR_NAVY, linewidth=2.3)
    ax4.axhline(92, color=COLOR_AMBER, linestyle="--", linewidth=1.4)
    style_axis(ax4, "Collection Rate %")
    ax4.set_ylim(60, 105)

    save_figure(fig, "executive_overview.png")


def expense_analysis(category: pd.DataFrame, monthly: pd.DataFrame) -> None:
    expenses = category[category["transaction_type"] == "Expense"].copy().head(8)
    fig = plt.figure(figsize=(14, 8), facecolor="#F7F9FA")
    fig.suptitle("Expense Analysis", x=0.06, y=0.95, ha="left", fontsize=18, fontweight="bold", color=COLOR_NAVY)
    fig.text(0.06, 0.915, "Category-level spend view for budget control and supplier review.", fontsize=10, color=COLOR_TEXT)

    ax1 = fig.add_axes([0.08, 0.50, 0.48, 0.32])
    ax1.barh(expenses["category"], expenses["total_aed"], color=COLOR_RED)
    ax1.invert_yaxis()
    style_axis(ax1, "Top Expense Categories")
    ax1.tick_params(axis="x", rotation=0)

    ax2 = fig.add_axes([0.64, 0.50, 0.26, 0.32])
    ax2.pie(expenses["total_aed"], labels=expenses["category"], autopct="%1.0f%%", startangle=90, textprops={"fontsize": 7})
    ax2.set_title("Spend Mix", loc="left", fontsize=12, fontweight="bold", color=COLOR_NAVY)

    ax3 = fig.add_axes([0.08, 0.12, 0.82, 0.25])
    ax3.bar(monthly["month"], monthly["expense_budget_aed"], color="#CFD8DC", label="Budget")
    ax3.bar(monthly["month"], monthly["expenses_aed"], color=COLOR_RED, label="Actual")
    style_axis(ax3, "Monthly Expense Budget vs Actual")
    ax3.legend(frameon=False, fontsize=9)

    save_figure(fig, "expense_analysis.png")


def revenue_trends(monthly: pd.DataFrame, customers: pd.DataFrame) -> None:
    top_customers = customers.sort_values("revenue_aed", ascending=False).head(8)
    fig = plt.figure(figsize=(14, 8), facecolor="#F7F9FA")
    fig.suptitle("Revenue Trends", x=0.06, y=0.95, ha="left", fontsize=18, fontweight="bold", color=COLOR_NAVY)
    fig.text(0.06, 0.915, "Revenue movement, customer contribution, and invoice volume for sales follow-up.", fontsize=10, color=COLOR_TEXT)

    ax1 = fig.add_axes([0.07, 0.52, 0.54, 0.30])
    ax1.fill_between(monthly["month"], monthly["revenue_aed"], color=COLOR_BLUE, alpha=0.18)
    ax1.plot(monthly["month"], monthly["revenue_aed"], color=COLOR_BLUE, marker="o", linewidth=2.5)
    style_axis(ax1, "Monthly Revenue")

    ax2 = fig.add_axes([0.69, 0.52, 0.24, 0.30])
    ax2.bar(monthly["month"], monthly["invoice_count"], color=COLOR_TEAL)
    style_axis(ax2, "Invoice Count")

    ax3 = fig.add_axes([0.09, 0.12, 0.80, 0.25])
    ax3.barh(top_customers["customer_name"], top_customers["revenue_aed"], color=COLOR_GREEN)
    ax3.invert_yaxis()
    style_axis(ax3, "Top Customers by Revenue")
    ax3.tick_params(axis="x", rotation=0)

    save_figure(fig, "revenue_trends.png")


def kpi_target_tracking(monthly: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(14, 8), facecolor="#F7F9FA")
    fig.suptitle("KPI Target Tracking", x=0.06, y=0.95, ha="left", fontsize=18, fontweight="bold", color=COLOR_NAVY)
    fig.text(0.06, 0.915, "Actual performance compared with monthly management targets.", fontsize=10, color=COLOR_TEXT)

    ax1 = fig.add_axes([0.08, 0.55, 0.38, 0.28])
    ax1.bar(monthly["month"], monthly["revenue_vs_target_pct"], color=COLOR_BLUE)
    ax1.axhline(100, color=COLOR_NAVY, linestyle="--", linewidth=1.2)
    style_axis(ax1, "Revenue vs Target %")

    ax2 = fig.add_axes([0.56, 0.55, 0.36, 0.28])
    colors = [COLOR_GREEN if v <= 100 else COLOR_RED for v in monthly["expense_budget_used_pct"]]
    ax2.bar(monthly["month"], monthly["expense_budget_used_pct"], color=colors)
    ax2.axhline(100, color=COLOR_NAVY, linestyle="--", linewidth=1.2)
    style_axis(ax2, "Expense Budget Used %")

    ax3 = fig.add_axes([0.08, 0.13, 0.38, 0.28])
    ax3.plot(monthly["month"], monthly["net_profit_aed"], color=COLOR_GREEN, marker="o", label="Actual")
    ax3.plot(monthly["month"], monthly["net_profit_target_aed"], color=COLOR_NAVY, linestyle="--", label="Target")
    style_axis(ax3, "Net Profit Actual vs Target")
    ax3.legend(frameon=False, fontsize=9)

    ax4 = fig.add_axes([0.56, 0.13, 0.36, 0.28])
    ax4.plot(monthly["month"], monthly["collection_rate_pct"], color=COLOR_TEAL, marker="o", label="Actual")
    ax4.axhline(92, color=COLOR_AMBER, linestyle="--", linewidth=1.4, label="Target")
    style_axis(ax4, "Collection Rate Target")
    ax4.set_ylim(60, 105)
    ax4.legend(frameon=False, fontsize=9)

    save_figure(fig, "kpi_target_tracking.png")


def workflow_diagram() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 4.2), facecolor="#F7F9FA")
    ax.axis("off")
    steps = [
        "Telegram /\nManual Input",
        "Automation\nEngine",
        "Data\nCleaning",
        "Google Sheets /\nDatabase",
        "KPI\nDashboard",
        "Management\nReport",
    ]
    x_positions = [0.10, 0.26, 0.42, 0.58, 0.74, 0.90]
    colors = [COLOR_BLUE, COLOR_TEAL, COLOR_AMBER, COLOR_NAVY, COLOR_GREEN, "#6A1B9A"]
    for i, (x, step, color) in enumerate(zip(x_positions, steps, colors)):
        box = FancyBboxPatch(
            (x - 0.06, 0.42),
            0.12,
            0.26,
            boxstyle="round,pad=0.02,rounding_size=0.025",
            linewidth=1.2,
            facecolor="white",
            edgecolor=color,
        )
        ax.add_patch(box)
        ax.text(x - 0.005, 0.55, step, ha="center", va="center", fontsize=10, fontweight="bold", color=COLOR_NAVY)
        if i < len(x_positions) - 1:
            ax.annotate(
                "",
                xy=(x_positions[i + 1] - 0.075, 0.55),
                xytext=(x + 0.06, 0.55),
                arrowprops=dict(arrowstyle="->", color=COLOR_TEXT, linewidth=1.8),
            )
    ax.text(0.02, 0.86, "Automated Business Reporting Workflow", fontsize=17, fontweight="bold", color=COLOR_NAVY)
    ax.text(0.02, 0.76, "A lightweight SME reporting pipeline from raw inputs to decision-ready management reporting.", fontsize=10, color=COLOR_TEXT)
    fig.savefig(ASSETS_DIR / "workflow_diagram.png", dpi=180, bbox_inches="tight", facecolor="#F7F9FA")
    plt.close(fig)


def main() -> None:
    monthly = pd.read_csv(DATA_DIR / "monthly_summary.csv")
    category = pd.read_csv(PROCESSED_DIR / "category_summary.csv")
    customers = pd.read_csv(PROCESSED_DIR / "customer_activity.csv")

    executive_overview(monthly)
    expense_analysis(category, monthly)
    revenue_trends(monthly, customers)
    kpi_target_tracking(monthly)
    workflow_diagram()
    print(f"Dashboard screenshots saved in {DASHBOARD_DIR}")
    print(f"Workflow diagram saved in {ASSETS_DIR}")


if __name__ == "__main__":
    main()
