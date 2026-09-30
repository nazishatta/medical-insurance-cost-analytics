# Medical Insurance Cost Explorer

An interactive healthcare analytics dashboard for exploring patterns in medical charges across age, body mass index, smoking status, and U.S. regions.

**Tech Stack:** Python · Pandas · Plotly · Streamlit

## Live Application

[![Open Live Dashboard](https://img.shields.io/badge/Open%20Live%20Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://medical-insurance-cost-analytics-09.streamlit.app/)

**Live Dashboard:** [medical-insurance-cost-analytics-09.streamlit.app](https://medical-insurance-cost-analytics-09.streamlit.app/)

Explore the deployed analytics dashboard directly in your browser. Use the interactive controls to filter the population by age, BMI, smoking status, and region; compare medical-charge patterns across multiple visualizations; inspect the underlying records; and export the filtered dataset for further analysis.

## Project Overview

The Medical Insurance Cost Explorer is a dark-themed interactive analytics application designed to make insurance-cost data easier to explore and interpret.

The application focuses on relationships between medical charges and several demographic or lifestyle-related variables contained in the dataset, including:

- Age
- Body mass index
- Smoking status
- Number of children
- U.S. region
- Recorded sex category
- Medical charges

Rather than presenting a static notebook or fixed chart, the dashboard allows users to interactively refine the dataset and immediately observe how metrics, charts, summaries, and exported records change.

## Key Features

- Filter records by age range.
- Filter records by BMI range.
- Filter by smoking status.
- Filter by U.S. region.
- Compare mean and median medical charges.
- View dynamic KPI metrics based on the filtered population.
- Explore age-versus-charges relationships.
- Explore BMI-versus-charges relationships.
- Compare regional medical-charge summaries.
- Inspect the filtered source records directly.
- Export only the currently filtered data to CSV.
- Use responsive sidebar controls that update every analytical view.
- Reuse validated source data through Streamlit caching for responsive interaction.
- View a built-in About section with data-quality notes and a data dictionary.
- Use a consistent dark visual theme across the dashboard and charts.

## Interactive Dashboard Design

The application uses a charcoal-gray visual system with restrained accent colors to create a professional analytics interface.

### Theme

- **Primary background:** `#111318`
- **Secondary background:** `#1b2028`
- **Primary accent:** `#6cdec9`
- **Secondary accent:** `#f5b76b`
- **Primary text:** `#e9eff4`
- **Muted text:** `#abb6c4`

The visual design is intended to maintain strong contrast while keeping analytical content readable across charts, filters, metrics, and data tables.

## Dashboard Structure

The application is organized into three main analytical views.

### Visualizations

The visualization section contains:

- Age vs. medical charges scatter plot
- BMI vs. medical charges scatter plot
- Regional mean or median charge comparison

The charts respond dynamically to all sidebar filters.

### Data & Export

The data section displays the filtered dataset used by the current dashboard state.

Users can export the filtered records using the built-in CSV download function.

### About

The About section provides:

- Dataset description
- Data-quality summary
- Source record count
- Missing-value count
- Duplicate-row count
- Data dictionary
- Interpretation guidance
- Analysis limitations

## Dataset

The project uses the bundled file:

```text
data/insurance.csv
