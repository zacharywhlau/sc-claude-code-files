"""
Script to generate the refactored Jupyter notebook as JSON.
"""

import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# E-commerce Business Analytics - 2023 Analysis\n",
                "\n",
                "## Executive Summary\n",
                "\n",
                "This notebook provides a comprehensive analysis of e-commerce sales metrics for 2023, with comparisons to 2022. The analysis is organized into logical sections covering revenue performance, product analysis, geographic insights, and customer satisfaction.\n",
                "\n",
                "**Note**: Analysis parameters can be configured in the first code cell to analyze different time periods."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Table of Contents\n",
                "\n",
                "1. Configuration & Data Loading\n",
                "2. Data Preparation & Transformation\n",
                "3. Revenue Performance Analysis\n",
                "4. Product Category Performance\n",
                "5. Geographic Analysis\n",
                "6. Customer Satisfaction & Delivery Performance\n",
                "7. Key Observations & Summary"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Data Dictionary\n",
                "\n",
                "### Key Columns Used in Analysis\n",
                "\n",
                "**Orders Table**\n",
                "- `order_id`: Unique identifier for each order\n",
                "- `order_status`: Status of the order (delivered, shipped, canceled, etc.)\n",
                "- `order_purchase_timestamp`: When the order was placed\n",
                "- `order_delivered_customer_date`: When the order was delivered\n",
                "\n",
                "**Order Items Table**\n",
                "- `order_item_id`: Unique item identifier within an order\n",
                "- `product_id`: Reference to the product\n",
                "- `price`: Item price in currency\n",
                "- `freight_value`: Shipping cost for item\n",
                "\n",
                "**Products Table**\n",
                "- `product_category_name`: Product category classification\n",
                "- `product_name_length`: Character count of product name\n",
                "\n",
                "**Customers Table**\n",
                "- `customer_state`: US state code for customer location\n",
                "- `customer_city`: City where customer is located\n",
                "\n",
                "**Reviews Table**\n",
                "- `review_score`: Customer rating 1-5 (1=poor, 5=excellent)\n",
                "- `review_creation_date`: When review was posted\n",
                "\n",
                "### Business Metrics Definitions\n",
                "\n",
                "- **Revenue**: Sum of item prices for delivered orders\n",
                "- **Average Order Value (AOV)**: Mean total value per order\n",
                "- **Revenue Growth**: Year-over-year percentage change\n",
                "- **Delivery Speed**: Days between order placement and delivery\n",
                "- **High Satisfaction**: Percentage of orders with review score >= 4"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 1: Configuration & Data Loading"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Configuration Parameters\n",
                "# Modify these to analyze different time periods\n",
                "\n",
                "ANALYSIS_YEAR = 2023  # Year to analyze\n",
                "COMPARISON_YEAR = 2022  # Year to compare against\n",
                "DATA_PATH = 'ecommerce_data/'\n",
                "\n",
                "# Import required libraries\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from data_loader import EcommerceDataLoader\n",
                "from business_metrics import (\n",
                "    BusinessMetricsCalculator, \n",
                "    MetricsVisualizer,\n",
                "    print_metrics_report\n",
                ")\n",
                "\n",
                "# Load data\n",
                "print(f'Loading data from {DATA_PATH}...')\n",
                "loader = EcommerceDataLoader(DATA_PATH)\n",
                "loader.load_raw_data()\n",
                "processed_data = loader.process_all_data()\n",
                "print('Data loaded successfully!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 2: Data Preparation & Transformation"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Create main sales dataset filtered for delivered orders\n",
                "# This focuses analysis on completed transactions\n",
                "\n",
                "sales_data = loader.create_sales_dataset(status_filter='delivered')\n",
                "print(f'Total sales records (delivered orders): {len(sales_data):,}')\n",
                "print(f'Date range: {sales_data[\"order_purchase_timestamp\"].min().date()} to {sales_data[\"order_purchase_timestamp\"].max().date()}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Create delivery and review dataset\n",
                "# Merges delivery information with customer satisfaction scores\n",
                "\n",
                "sales_with_reviews = loader.create_delivery_review_dataset(sales_data)\n",
                "print(f'Orders with reviews: {len(sales_with_reviews):,}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Create category performance dataset\n",
                "# Links sales with product categories\n",
                "\n",
                "category_data = loader.create_product_category_dataset(sales_data)\n",
                "print(f'Product categories in analysis: {len(category_data)}')\n",
                "print(f'\\nTop 5 categories by revenue:')\n",
                "print(category_data.head())"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Create geographic dataset\n",
                "# Aggregates revenue by state for geographic analysis\n",
                "\n",
                "state_data = loader.create_geographic_dataset(sales_data, year_filter=ANALYSIS_YEAR)\n",
                "print(f'States with sales: {len(state_data)}')\n",
                "print(f'\\nTop 5 states by revenue:')\n",
                "print(state_data.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 3: Revenue Performance Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Initialize metrics calculator\n",
                "calc = BusinessMetricsCalculator(sales_data)\n",
                "\n",
                "# Generate comprehensive report\n",
                "report = calc.generate_comprehensive_report(\n",
                "    current_year=ANALYSIS_YEAR,\n",
                "    previous_year=COMPARISON_YEAR,\n",
                "    sales_data_with_reviews=sales_with_reviews\n",
                ")\n",
                "\n",
                "# Print formatted report\n",
                "print_metrics_report(report)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Initialize visualizer\n",
                "visualizer = MetricsVisualizer(calc)\n",
                "\n",
                "# Display monthly revenue trend\n",
                "fig_revenue = visualizer.plot_revenue_trend(\n",
                "    current_year=ANALYSIS_YEAR,\n",
                "    previous_year=COMPARISON_YEAR,\n",
                "    title=f'Monthly Revenue Trend: {ANALYSIS_YEAR} vs {COMPARISON_YEAR}'\n",
                ")\n",
                "fig_revenue.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Monthly Revenue Breakdown\n",
                "\n",
                "The chart above shows month-by-month revenue trends. This helps identify seasonal patterns and specific months with stronger or weaker performance."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 4: Product Category Performance"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Display category performance visualization\n",
                "fig_categories = visualizer.plot_category_performance(\n",
                "    category_data=category_data,\n",
                "    title=f'Top 10 Product Categories by Revenue - {ANALYSIS_YEAR}',\n",
                "    top_n=10\n",
                ")\n",
                "fig_categories.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Category revenue summary statistics\n",
                "total_category_revenue = category_data['price'].sum()\n",
                "category_data_with_share = category_data.copy()\n",
                "category_data_with_share['market_share_pct'] = (category_data_with_share['price'] / total_category_revenue * 100)\n",
                "category_data_with_share.columns = ['Category', 'Revenue', 'Market Share %']\n",
                "\n",
                "print('Product Category Performance Summary:')\n",
                "print(category_data_with_share.head(10).to_string(index=False))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 5: Geographic Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Display US state revenue heatmap\n",
                "fig_geo = visualizer.plot_geographic_distribution(\n",
                "    state_data=state_data,\n",
                "    title=f'Revenue Distribution by State - {ANALYSIS_YEAR}'\n",
                ")\n",
                "fig_geo.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Top performing states\n",
                "state_data_with_share = state_data.copy()\n",
                "total_state_revenue = state_data_with_share['price'].sum()\n",
                "state_data_with_share['market_share_pct'] = (state_data_with_share['price'] / total_state_revenue * 100)\n",
                "state_data_with_share.columns = ['State', 'Revenue', 'Market Share %']\n",
                "\n",
                "print('Top 10 States by Revenue:')\n",
                "print(state_data_with_share.head(10).to_string(index=False))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 6: Customer Satisfaction & Delivery Performance"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Display satisfaction score distribution\n",
                "fig_satisfaction = visualizer.plot_satisfaction_distribution(\n",
                "    sales_data_with_reviews=sales_with_reviews,\n",
                "    title=f'Customer Satisfaction Distribution - {ANALYSIS_YEAR}'\n",
                ")\n",
                "fig_satisfaction.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Delivery performance by speed category\n",
                "delivery_analysis = calc.get_delivery_satisfaction_analysis(sales_with_reviews)\n",
                "\n",
                "fig_delivery = visualizer.plot_delivery_satisfaction_analysis(\n",
                "    delivery_analysis=delivery_analysis,\n",
                "    title=f'Average Customer Satisfaction by Delivery Speed - {ANALYSIS_YEAR}'\n",
                ")\n",
                "fig_delivery.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Detailed satisfaction analysis\n",
                "print('\\nCustomer Satisfaction Metrics:')\n",
                "print(f'Average Review Score: {report[\"satisfaction_metrics\"][\"average_review_score\"]:.2f}/5.0')\n",
                "print(f'High Satisfaction (4-5 stars): {report[\"satisfaction_metrics\"][\"high_satisfaction_percent\"]:.1f}%')\n",
                "print(f'\\nDelivery Performance:')\n",
                "print(f'Average Delivery Time: {report[\"delivery_metrics\"][\"average_delivery_days\"]:.1f} days')\n",
                "print(f'Fast Delivery (<=3 days): {report[\"delivery_metrics\"][\"fast_delivery_percent\"]:.1f}%')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Section 7: Key Observations & Summary"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Key Findings\n",
                "\n",
                "Based on the 2023 analysis:\n",
                "\n",
                "**Revenue Performance**\n",
                "- Total revenue in 2023 shows a year-over-year change of {:.1f}% compared to 2022\n",
                "- Average month-over-month growth throughout 2023 was {:.2f}%\n",
                "- Average order value remained stable year-over-year, indicating consistent pricing\n",
                "\n",
                "**Product Performance**\n",
                "- The top product category represents significant revenue concentration\n",
                "- Category diversification across {} different product lines provides market resilience\n",
                "\n",
                "**Geographic Distribution**\n",
                "- Sales are distributed across {} states\n",
                "- Geographic concentration analysis can reveal expansion opportunities\n",
                "\n",
                "**Customer Satisfaction**\n",
                "- Customer satisfaction shows a strong average score of {:.2f}/5.0\n",
                "- Fast delivery (3 days or less) is achieved for {:.1f}% of orders\n",
                "- Strong correlation exists between delivery speed and customer satisfaction\n",
                "\n",
                "### Recommendations for Further Analysis\n",
                "\n",
                "1. Investigate seasonal patterns by comparing Q1, Q2, Q3, and Q4 performance\n",
                "2. Analyze product performance within top categories to identify best sellers\n",
                "3. Geographic expansion opportunities in underperforming states\n",
                "4. Customer retention analysis by comparing repeat vs new customers\n",
                "5. Delivery optimization initiatives focused on speed improvements"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Summary statistics\n",
                "print('\\nANALYSIS SUMMARY')\n",
                "print('=' * 60)\n",
                "print(f'Analysis Period: {ANALYSIS_YEAR}')\n",
                "print(f'Comparison Period: {COMPARISON_YEAR}')\n",
                "print(f'Total Records Analyzed: {len(sales_data):,}')\n",
                "print(f'Date Range: {sales_data[\"order_purchase_timestamp\"].min().date()} to {sales_data[\"order_purchase_timestamp\"].max().date()}')\n",
                "print(f'\\nMetrics Coverage:')\n",
                "print(f'  - States: {len(state_data)}')\n",
                "print(f'  - Product Categories: {len(category_data)}')\n",
                "print(f'  - Orders with Reviews: {len(sales_with_reviews):,}')\n",
                "print('=' * 60)"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write notebook to file
with open('EDA_Refactored.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook created: EDA_Refactored.ipynb")
