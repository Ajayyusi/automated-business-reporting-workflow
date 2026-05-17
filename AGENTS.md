# AGENTS.md

## Project Purpose

This repository is a portfolio project for a Business Intelligence Analyst | Data & Automation Specialist profile. It demonstrates a practical automated reporting workflow for a UAE SME service business using Python, pandas, SQL, CSV files, and dashboard screenshots.

The business message should remain clear: this project improves business operations using data, dashboards, and automation.

## Folder Structure

- `data/` contains generated synthetic source data and processed reporting outputs.
- `src/` contains Python scripts for data generation, cleaning, KPI reporting, and dashboard image creation.
- `sql/` contains schema and analysis queries.
- `dashboards/` contains generated dashboard screenshots and report output tables.
- `workflow/` contains notes about the reporting pipeline.
- `docs/` contains business documentation and the data dictionary.
- `assets/` contains visual assets such as the workflow diagram.

## Coding Style

- Keep scripts simple, readable, and suitable for a junior BI/data automation portfolio.
- Use Python, pandas, matplotlib, CSV, SQL, and Markdown.
- Avoid heavy frameworks unless there is a clear reason.
- Prefer explicit column names and readable transformations over clever one-liners.
- Keep all currency values in AED.
- Treat sample data as synthetic and safe to publish.

## How to Run Scripts

From the repository root:

```bash
pip install -r requirements.txt
python src/generate_sample_data.py
python src/clean_transform_data.py
python src/generate_kpi_report.py
python src/create_dashboard_screenshots.py
```

## How to Update Data

1. Edit `src/generate_sample_data.py` to adjust customers, categories, targets, or transaction ranges.
2. Run `python src/generate_sample_data.py`.
3. Run `python src/clean_transform_data.py`.
4. Run `python src/generate_kpi_report.py`.
5. Run `python src/create_dashboard_screenshots.py`.
6. Check that all CSV and PNG outputs still make sense for a UAE SME service business.

## How to Validate Outputs

Before committing changes:

- Confirm the six main CSV files exist in `data/`.
- Confirm cleaned outputs exist in `data/processed/`.
- Confirm dashboard images exist in `dashboards/`.
- Confirm the workflow diagram exists at `assets/workflow_diagram.png`.
- Open `README.md` and verify all image links point to existing files.
- Review KPI totals for believable values and no missing dates.

## Documentation Guidelines

- Keep the README business-focused and recruiter-friendly.
- Do not oversell the project as enterprise-level consulting work.
- Make it clear that the data is synthetic and anonymized.
- Maintain the career positioning: Business Intelligence Analyst | Data & Automation Specialist.
