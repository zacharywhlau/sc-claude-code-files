# Quick Reference Card

## Getting Started (30 seconds)

```bash
cd lesson7_files
jupyter notebook EDA_Refactored.ipynb
# Run all cells (Ctrl+Shift+Enter)
```

## Core Imports

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer
```

## Data Loading

```python
# Standard approach
loader = EcommerceDataLoader('ecommerce_data/')
loader.load_raw_data()

# Get specific dataset
sales_2023 = loader.create_sales_dataset(year_filter=2023, status_filter='delivered')
sales_april = loader.create_sales_dataset(year_filter=2023, month_filter=4)

# Specific analyses
categories = loader.create_product_category_dataset(sales_2023)
states = loader.create_geographic_dataset(sales_2023)
delivery = loader.create_delivery_review_dataset(sales_2023)
```

## Metrics Calculation

```python
calc = BusinessMetricsCalculator(sales_data)

# Single metrics
revenue_growth = calc.calculate_revenue_growth(2023, 2022)
monthly_avg = calc.calculate_average_monthly_growth(2023)
satisfaction = calc.calculate_satisfaction_metrics(sales_with_reviews)
delivery = calc.calculate_delivery_metrics(sales_with_reviews)

# Comprehensive report
report = calc.generate_comprehensive_report(2023, 2022, sales_with_reviews)

# Print formatted output
from business_metrics import print_metrics_report
print_metrics_report(report)
```

## Visualizations

```python
visualizer = MetricsVisualizer(calc)

# Revenue comparison
fig = visualizer.plot_revenue_trend(2023, 2022)

# Categories
fig = visualizer.plot_category_performance(category_data, top_n=10)

# Geographic
fig = visualizer.plot_geographic_distribution(state_data)

# Satisfaction
fig = visualizer.plot_satisfaction_distribution(sales_with_reviews)

# Delivery analysis
delivery_analysis = calc.get_delivery_satisfaction_analysis(sales_with_reviews)
fig = visualizer.plot_delivery_satisfaction_analysis(delivery_analysis)

# Show all
fig.show()
```

## Key Metrics

| Metric | Calculation | Example |
|--------|-------------|---------|
| Total Revenue | Sum of order prices | $3.4M |
| AOV | Mean order total | $724.98 |
| Revenue Growth | (Current - Previous) / Previous * 100 | -2.46% |
| Avg Review Score | Mean of ratings (1-5) | 4.10 |
| Delivery Speed | Days from order to delivery | 8.0 |
| High Satisfaction | % of orders with 4+ stars | 84% |

## Dataset Structure

```
Orders
├── order_id (unique identifier)
├── order_status (delivered, shipped, etc)
├── order_purchase_timestamp (order date)
└── order_delivered_customer_date (delivery date)

Order Items
├── order_id (links to orders)
├── product_id (links to products)
├── price (item price)
└── freight_value (shipping cost)

Products
├── product_id (unique identifier)
└── product_category_name (category)

Customers
├── customer_id (unique identifier)
└── customer_state (US state)

Reviews
├── order_id (links to orders)
└── review_score (1-5 rating)
```

## Analysis Workflow

```python
# 1. Load data
loader = EcommerceDataLoader('ecommerce_data/')
loader.load_raw_data()

# 2. Create filtered dataset
sales = loader.create_sales_dataset(year_filter=2023)

# 3. Create support datasets
categories = loader.create_product_category_dataset(sales)
states = loader.create_geographic_dataset(sales)
reviews = loader.create_delivery_review_dataset(sales)

# 4. Calculate metrics
calc = BusinessMetricsCalculator(sales)
report = calc.generate_comprehensive_report(2023, 2022, reviews)

# 5. Visualize
visualizer = MetricsVisualizer(calc)
fig1 = visualizer.plot_revenue_trend(2023, 2022)
fig2 = visualizer.plot_category_performance(categories)
fig1.show()
fig2.show()

# 6. Print report
print_metrics_report(report)
```

## Configuration Options

```python
# In notebook or script
ANALYSIS_YEAR = 2023          # Year to analyze
COMPARISON_YEAR = 2022        # Comparison year
DATA_PATH = 'ecommerce_data/' # Data location
```

## Common Filters

```python
# By year
loader.create_sales_dataset(year_filter=2023)

# By month (1-12)
loader.create_sales_dataset(month_filter=10)

# By status
loader.create_sales_dataset(status_filter='delivered')

# Combined
loader.create_sales_dataset(
    year_filter=2023,
    month_filter=4,
    status_filter='delivered'
)
```

## Utility Functions

```python
from business_metrics import format_currency, print_metrics_report

# Format currency
formatted = format_currency(3360294.74)  # "$3.4M"

# Print report
print_metrics_report(report)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run from lesson7_files directory |
| Empty data | Check year/month filters match data |
| No visualization | Install plotly: `pip install plotly` |
| Slow performance | Filter by specific month/year |
| Wrong results | Verify status_filter='delivered' |

## File Locations

- Refactored notebook: `EDA_Refactored.ipynb`
- Data loader module: `data_loader.py`
- Metrics module: `business_metrics.py`
- Full documentation: `README.md`
- Usage guide: `USAGE_GUIDE.md`
- Data files: `ecommerce_data/`

## Key Statistics (2023 Analysis)

- Total Revenue: $3.36M
- Total Orders: 4,635
- Product Categories: 13
- States with Sales: 50
- Average Delivery Time: 8.0 days
- Average Review Score: 4.10/5.0
- Revenue Growth (YoY): -2.46%

## Accessing Results from Report

```python
report = calc.generate_comprehensive_report(2023, 2022, sales_with_reviews)

# Access metrics
revenue = report['current_year_metrics']['total_revenue']
orders = report['order_metrics']['total_orders']
growth = report['revenue_growth']
satisfaction = report['satisfaction_metrics']['average_review_score']
delivery = report['delivery_metrics']['average_delivery_days']
monthly_growth = report['monthly_growth']
```

## Next Steps

1. Read `USAGE_GUIDE.md` for detailed examples
2. See `README.md` for full documentation
3. Check `prompt.md` for refactoring details
4. Explore `EDA_Refactored.ipynb` for complete analysis

---

**Pro Tip**: Save this page as a browser bookmark or print it for quick reference while working with the analysis framework.
