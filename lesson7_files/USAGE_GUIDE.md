# Refactored Analysis - Usage Guide

## Quick Start

### 1. Run the Refactored Notebook

```bash
jupyter notebook EDA_Refactored.ipynb
```

Select the "Lesson 7" kernel and run all cells to generate the complete 2023 analysis.

### 2. Analyze a Different Year

Edit the configuration cell at the top of the notebook:

```python
ANALYSIS_YEAR = 2023  # Change to desired year
COMPARISON_YEAR = 2022  # Change to desired comparison year
```

Then run all cells again to regenerate all metrics and visualizations.

### 3. Import Modules in Your Code

```python
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer, print_metrics_report

# Quick start
loader, processed_data = load_and_process_data('ecommerce_data/')
```

## Module Guide

### data_loader.py

**Purpose**: Load, clean, and prepare e-commerce datasets

**Main Class**: `EcommerceDataLoader`

```python
# Initialize loader
loader = EcommerceDataLoader('ecommerce_data/')

# Load all raw data
loader.load_raw_data()

# Get processed data dictionary
processed_data = loader.process_all_data()
# Returns: {
#     'orders': DataFrame with datetime fields and year/month columns
#     'order_items': DataFrame with price and freight data
#     'products': DataFrame with category information
#     'customers': DataFrame with location data
#     'reviews': DataFrame with review scores
# }

# Create filtered sales dataset
sales_data = loader.create_sales_dataset(
    year_filter=2023,      # Optional: filter by year
    month_filter=None,     # Optional: filter by month (1-12)
    status_filter='delivered'  # Filter by order status
)

# Create geographic analysis dataset
state_data = loader.create_geographic_dataset(
    sales_data=sales_data,
    year_filter=2023
)

# Create category performance dataset
category_data = loader.create_product_category_dataset(sales_data)

# Create delivery and review dataset
delivery_reviews = loader.create_delivery_review_dataset(sales_data)
```

### business_metrics.py

**Purpose**: Calculate metrics and create visualizations

**Main Classes**:
- `BusinessMetricsCalculator`: Compute all business metrics
- `MetricsVisualizer`: Create professional visualizations

**Example Usage**:

```python
# Initialize calculator
calc = BusinessMetricsCalculator(sales_data)

# Calculate revenue metrics for a year
metrics = calc.calculate_revenue_metrics(2023)
# Returns: {
#     'total_revenue': float,
#     'total_orders': int,
#     'average_order_value': float
# }

# Calculate year-over-year growth
growth = calc.calculate_revenue_growth(2023, 2022)  # Returns percentage

# Calculate monthly growth trend
monthly_growth = calc.calculate_monthly_growth(2023)  # Returns Series

# Get monthly revenue breakdown
monthly_data = calc.get_monthly_revenue(2023)

# Calculate satisfaction metrics
satisfaction = calc.calculate_satisfaction_metrics(sales_with_reviews)

# Calculate delivery metrics
delivery = calc.calculate_delivery_metrics(sales_with_reviews)

# Generate comprehensive report
report = calc.generate_comprehensive_report(
    current_year=2023,
    previous_year=2022,
    sales_data_with_reviews=sales_with_reviews
)

# Create visualizations
visualizer = MetricsVisualizer(calc)

# Revenue trend chart
fig = visualizer.plot_revenue_trend(2023, 2022)
fig.show()

# Category performance
fig = visualizer.plot_category_performance(category_data, top_n=10)
fig.show()

# Geographic distribution
fig = visualizer.plot_geographic_distribution(state_data)
fig.show()

# Satisfaction distribution
fig = visualizer.plot_satisfaction_distribution(sales_with_reviews)
fig.show()

# Delivery vs satisfaction
delivery_analysis = calc.get_delivery_satisfaction_analysis(sales_with_reviews)
fig = visualizer.plot_delivery_satisfaction_analysis(delivery_analysis)
fig.show()

# Print formatted report
print_metrics_report(report)
```

## Common Analysis Scenarios

### Scenario 1: Analyze Q4 Performance

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetricsCalculator

loader = EcommerceDataLoader('ecommerce_data/')
loader.load_raw_data()

# Get Q4 sales
sales_q4 = loader.create_sales_dataset(year_filter=2023)
q4_data = sales_q4[sales_q4['month'].isin([10, 11, 12])]

# Calculate metrics
calc = BusinessMetricsCalculator(q4_data)
revenue = q4_data['price'].sum()
orders = q4_data['order_id'].nunique()

print(f"Q4 Revenue: ${revenue:,.2f}")
print(f"Q4 Orders: {orders:,}")
```

### Scenario 2: Compare Specific Categories

```python
# Get top 5 categories
top_categories = category_data.head(5)['price'].index

# Filter sales for top categories
top_sales = sales_data[sales_data['product_id'].isin(
    loader.products[loader.products['product_category_name'].isin(
        top_categories
    )]['product_id']
)]

# Analyze performance
print(top_sales.groupby('year')['price'].sum())
```

### Scenario 3: Geographic Deep Dive

```python
# Get top state
top_state = state_data.iloc[0]['price']  # State name column

# Analyze by month
state_monthly = state_data.groupby('month')['price'].sum()

# Compare to national average
national_avg = sales_data['price'].mean()
state_avg = sales_data[sales_data['customer_state'] == top_state]['price'].mean()

print(f"State AOV: ${state_avg:.2f}")
print(f"National AOV: ${national_avg:.2f}")
```

### Scenario 4: Customer Satisfaction Analysis

```python
# Satisfaction by product category
category_satisfaction = sales_with_reviews.merge(
    products,
    on='product_id'
).groupby('product_category_name')['review_score'].mean()

print(category_satisfaction.sort_values(ascending=False))
```

### Scenario 5: Delivery Time Optimization

```python
# Get delivery metrics by state
state_delivery = sales_with_reviews.merge(
    orders,
    on='order_id'
).merge(
    customers,
    on='customer_id'
).groupby('customer_state')['delivery_speed'].mean()

# Find slowest states
slowest_states = state_delivery.nlargest(5)
print("Slowest delivering states:")
print(slowest_states)
```

## Customization Examples

### Add Custom Metric

```python
class CustomMetricsCalculator(BusinessMetricsCalculator):
    def calculate_seasonal_index(self, year: int) -> dict:
        """Calculate seasonal index for each month."""
        year_data = self.sales_data[self.sales_data['year'] == year]
        monthly_avg = year_data.groupby('month')['price'].mean()
        overall_avg = monthly_avg.mean()
        return (monthly_avg / overall_avg).to_dict()

# Use it
calc = CustomMetricsCalculator(sales_data)
seasonal = calc.calculate_seasonal_index(2023)
```

### Add Custom Visualization

```python
class CustomVisualizer(MetricsVisualizer):
    def plot_revenue_vs_orders(self, year: int):
        """Scatter plot of revenue vs order count by month."""
        monthly_data = self.calc.get_monthly_revenue(year)
        monthly_orders = self.calc.sales_data[
            self.calc.sales_data['year'] == year
        ].groupby('month')['order_id'].nunique().reset_index()
        
        fig = px.scatter(
            x=monthly_orders['order_id'],
            y=monthly_data['revenue'],
            title=f'Revenue vs Order Count - {year}',
            labels={'x': 'Order Count', 'y': 'Revenue ($)'}
        )
        return fig

# Use it
visualizer = CustomVisualizer(calc)
fig = visualizer.plot_revenue_vs_orders(2023)
fig.show()
```

### Filter by Multiple Conditions

```python
# Complex filtering
sales_filtered = sales_data[
    (sales_data['year'] == 2023) &
    (sales_data['month'].isin([10, 11, 12])) &
    (sales_data['price'] > 500)
]

# Then analyze
print(f"High-value Q4 orders: {sales_filtered['order_id'].nunique()}")
print(f"Total revenue: ${sales_filtered['price'].sum():,.2f}")
```

## Output Examples

### Console Output

```
BUSINESS METRICS SUMMARY - 2023
============================================================

REVENUE PERFORMANCE:
  Total Revenue: $3.4M
  Total Orders: 4,635
  Average Order Value: $724.98
  Revenue Growth: -2.5%
  Monthly Growth Trend: -0.39%

CUSTOMER SATISFACTION:
  Average Review Score: 4.10/5.0
  High Satisfaction (4+): 84.2%

DELIVERY PERFORMANCE:
  Average Delivery Time: 8.0 days
  Fast Delivery (<=3 days): 28.5%

============================================================
```

### Visualization Outputs

- Interactive line charts for revenue trends
- Horizontal bar charts for category performance
- Geographic choropleth maps for state analysis
- Bar charts for satisfaction distribution
- Multiple chart types for multi-dimensional analysis

## Troubleshooting

### "No module named 'data_loader'"

Make sure you're running the notebook from the correct directory:
```bash
cd /path/to/lesson7_files
jupyter notebook EDA_Refactored.ipynb
```

### "KeyError" for column names

Verify the data files are correct CSV files with expected columns:
```python
loader.load_raw_data()
print(loader.orders.columns)
print(loader.order_items.columns)
```

### Empty results

Check your date filters match available data:
```python
# Check data range
print(sales_data['year'].unique())
print(sales_data['month'].unique())
```

### Visualizations don't display

Ensure Plotly is installed:
```bash
pip install plotly>=5.0.0
```

## Next Steps

1. **Explore the Data**: Run the refactored notebook to understand the analyses
2. **Customize Parameters**: Change ANALYSIS_YEAR and rerun
3. **Build Custom Metrics**: Extend classes for your specific needs
4. **Integrate Modules**: Use data_loader and business_metrics in other projects
5. **Automate Reports**: Build scripts that run analyses on schedule

## Additional Resources

- See README.md for full documentation
- See prompt.md for refactoring details
- Original EDA.ipynb preserved for reference
- All docstrings include detailed parameter and return value information
