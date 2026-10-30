"""
Professional Streamlit Dashboard for E-commerce Business Analytics
Converts the refactored EDA notebook into an interactive web dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer


# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .metric-trend {
        font-size: 16px;
        margin-top: 10px;
    }
    .trend-positive {
        color: #00cc96;
    }
    .trend-negative {
        color: #ef553b;
    }
</style>
""", unsafe_allow_html=True)


# Cache data loading
@st.cache_resource
def load_data(data_path='ecommerce_data/'):
    loader = EcommerceDataLoader(data_path)
    loader.load_raw_data()
    return loader


def format_currency_short(value):
    """Format currency as $300K or $2M"""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.0f}K"
    else:
        return f"${value:.0f}"


def create_metric_card(label, value, trend_value=None, is_positive=True):
    """Create a metric card with optional trend indicator"""
    if trend_value is not None:
        trend_color = "#00cc96" if (trend_value >= 0 and is_positive) or (trend_value < 0 and not is_positive) else "#ef553b"
        trend_arrow = "↑" if trend_value >= 0 else "↓"
        trend_text = f'<span style="color: {trend_color};">{trend_arrow} {abs(trend_value):.2f}%</span>'
        return f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">{label}</div>
            <div style="font-size: 28px; font-weight: bold; color: #333; margin-bottom: 12px;">{value}</div>
            <div style="font-size: 14px;">{trend_text}</div>
        </div>
        """
    else:
        return f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">{label}</div>
            <div style="font-size: 28px; font-weight: bold; color: #333;">{value}</div>
        </div>
        """


# Main app
st.markdown("# E-commerce Business Analytics Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")

analysis_year = st.sidebar.selectbox(
    "Select Year",
    [2023, 2022],
    index=0,
    key="analysis_year"
)

analysis_month = st.sidebar.selectbox(
    "Select Month (Optional)",
    [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    index=0,
    format_func=lambda x: "All Months" if x is None else f"Month {x}",
    key="analysis_month"
)

# Header
st.markdown("# E-commerce Business Analytics Dashboard")
st.markdown("### Sales Performance Analysis")

# Load data
loader = load_data()

# Create datasets with month filter
sales_data = loader.create_sales_dataset(
    year_filter=analysis_year,
    month_filter=analysis_month,
    status_filter='delivered'
)
sales_with_reviews = loader.create_delivery_review_dataset(sales_data)
category_data = loader.create_product_category_dataset(sales_data)
state_data = loader.create_geographic_dataset(sales_data, year_filter=analysis_year)

# Determine comparison year
comparison_year = 2022 if analysis_year == 2023 else 2021

# Calculate metrics
calc = BusinessMetricsCalculator(sales_data)
report = calc.generate_comprehensive_report(
    current_year=analysis_year,
    previous_year=comparison_year,
    sales_data_with_reviews=sales_with_reviews
)

# Get previous year metrics for comparison
previous_metrics = calc.calculate_revenue_metrics(comparison_year)
previous_aov = previous_metrics['average_order_value']
previous_orders = previous_metrics['total_orders']

# Calculate trends (with zero-division protection)
aov_trend = ((report['current_year_metrics']['average_order_value'] - previous_aov) / previous_aov * 100) if previous_aov > 0 else 0
orders_trend = ((report['order_metrics']['total_orders'] - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0

# KPI Row (4 columns)
st.markdown("---")
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    revenue_value = format_currency_short(report['current_year_metrics']['total_revenue'])
    st.markdown(
        create_metric_card(
            "Total Revenue",
            revenue_value,
            report['revenue_growth'],
            is_positive=True
        ),
        unsafe_allow_html=True
    )

with col2:
    growth_value = f"{report['monthly_growth']:.2f}%"
    st.markdown(
        create_metric_card(
            "Monthly Growth Trend",
            growth_value,
            None
        ),
        unsafe_allow_html=True
    )

with col3:
    aov_value = format_currency_short(report['current_year_metrics']['average_order_value'])
    st.markdown(
        create_metric_card(
            "Average Order Value",
            aov_value,
            aov_trend,
            is_positive=True
        ),
        unsafe_allow_html=True
    )

with col4:
    orders_value = f"{report['order_metrics']['total_orders']:,}"
    st.markdown(
        create_metric_card(
            "Total Orders",
            orders_value,
            orders_trend,
            is_positive=True
        ),
        unsafe_allow_html=True
    )

# Charts Grid (2x2)

chart_col1, chart_col2 = st.columns(2, gap="medium")

# Chart 1: Revenue Trend
with chart_col1:
    current_monthly = calc.get_monthly_revenue(analysis_year)
    previous_monthly = calc.get_monthly_revenue(comparison_year)

    fig_revenue = go.Figure()

    # Current year line (solid)
    fig_revenue.add_trace(go.Scatter(
        x=current_monthly['month'],
        y=current_monthly['revenue'],
        mode='lines+markers',
        name=str(analysis_year),
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    # Previous year line (dashed)
    fig_revenue.add_trace(go.Scatter(
        x=previous_monthly['month'],
        y=previous_monthly['revenue'],
        mode='lines+markers',
        name=str(comparison_year),
        line=dict(color='#ff7f0e', width=2, dash='dash'),
        marker=dict(size=6)
    ))

    fig_revenue.update_layout(
        title=f"Revenue Trend: {analysis_year} vs {comparison_year}",
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode='x unified',
        height=400,
        showlegend=True,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            tickformat='$,.0f'
        ),
        template='plotly_white'
    )

    # Format y-axis to show K/M format
    fig_revenue.update_yaxes(tickformat='$')

    st.plotly_chart(fig_revenue, use_container_width=True)

# Chart 2: Top 10 Categories (blue gradient)
with chart_col2:
    category_display = category_data.head(10).copy()
    category_display.columns = ['category', 'revenue']

    fig_categories = go.Figure()
    fig_categories.add_trace(go.Bar(
        x=category_display['revenue'],
        y=category_display['category'],
        orientation='h',
        marker=dict(
            color=category_display['revenue'],
            colorscale='Blues',
            showscale=False
        ),
        text=[format_currency_short(x) for x in category_display['revenue']],
        textposition='auto',
    ))

    fig_categories.update_layout(
        title=f"Top 10 Product Categories - {analysis_year}",
        xaxis_title="Revenue",
        yaxis_title="Category",
        height=400,
        showlegend=False,
        xaxis=dict(tickformat='$,.0f'),
        template='plotly_white'
    )

    st.plotly_chart(fig_categories, use_container_width=True)

# Second row of charts
chart_col3, chart_col4 = st.columns(2, gap="medium")

# Chart 3: Revenue by State (choropleth)
with chart_col3:
    state_display = state_data.copy()
    state_display.columns = ['state', 'revenue']

    fig_geo = px.choropleth(
        state_display,
        locations='state',
        color='revenue',
        locationmode='USA-states',
        scope='usa',
        color_continuous_scale='Blues',
        title=f"Revenue Distribution by State - {analysis_year}",
        labels={'revenue': 'Revenue ($)'}
    )

    fig_geo.update_layout(
        height=400,
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(243, 243, 243)'
        ),
        coloraxis_colorbar=dict(
            tickformat='$,.0f'
        )
    )

    st.plotly_chart(fig_geo, use_container_width=True)

# Chart 4: Satisfaction vs Delivery Time
with chart_col4:
    delivery_analysis = calc.get_delivery_satisfaction_analysis(sales_with_reviews)
    delivery_analysis.columns = ['delivery_category', 'avg_score']

    fig_satisfaction = go.Figure()
    fig_satisfaction.add_trace(go.Bar(
        x=delivery_analysis['delivery_category'],
        y=delivery_analysis['avg_score'],
        marker=dict(
            color=delivery_analysis['avg_score'],
            colorscale='Viridis',
            showscale=False,
            line=dict(color='white', width=2)
        ),
        text=[f"{x:.2f}" for x in delivery_analysis['avg_score']],
        textposition='auto',
    ))

    fig_satisfaction.update_layout(
        title=f"Average Satisfaction by Delivery Speed - {analysis_year}",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        height=400,
        showlegend=False,
        yaxis=dict(range=[0, 5]),
        template='plotly_white'
    )

    st.plotly_chart(fig_satisfaction, use_container_width=True)

# Bottom Row (2 cards)

bottom_col1, bottom_col2 = st.columns(2, gap="medium")

with bottom_col1:
    delivery_value = f"{report['delivery_metrics']['average_delivery_days']:.1f} days"
    st.markdown(
        create_metric_card(
            "Average Delivery Time",
            delivery_value,
            None
        ),
        unsafe_allow_html=True
    )

with bottom_col2:
    review_score = report['satisfaction_metrics']['average_review_score']
    stars = "★" * int(review_score) + ("☆" if review_score % 1 >= 0.5 else "")
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="font-size: 14px; color: #666; margin-bottom: 8px;">Average Review Score</div>
        <div style="font-size: 48px; font-weight: bold; color: #ffd700; margin: 10px 0;">{review_score:.2f}</div>
        <div style="font-size: 20px; color: #ffd700; letter-spacing: 4px;">{stars}</div>
        <div style="font-size: 12px; color: #999; margin-top: 10px;">out of 5.0 stars</div>
    </div>
    """, unsafe_allow_html=True)

# Footer summary
st.markdown("---")
st.markdown("### Summary")

summary_cols = st.columns(3)

with summary_cols[0]:
    st.metric("Analysis Period", f"{analysis_year}")

with summary_cols[1]:
    st.metric("Total Records", f"{len(sales_data):,}")

with summary_cols[2]:
    st.metric("Data Coverage", f"50 states, 13 categories")

# Footer note
st.markdown("""
---
*Dashboard last updated: Analysis based on delivered orders. Metrics calculated using business_metrics module.*
""")
