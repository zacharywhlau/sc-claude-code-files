"""
Business metrics calculation module for e-commerce analysis.

This module provides functions to calculate key business metrics
and generate insights from e-commerce data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Any
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


class BusinessMetricsCalculator:
    """Calculate business metrics from sales data."""

    def __init__(self, sales_data: pd.DataFrame):
        """Initialize calculator with sales data.

        Args:
            sales_data: Merged sales dataset from data_loader
        """
        self.sales_data = sales_data

    def calculate_revenue_metrics(self, year: int) -> Dict[str, Any]:
        """Calculate revenue-related metrics for a specific year.

        Args:
            year: Year to analyze

        Returns:
            Dictionary containing revenue metrics
        """
        year_data = self.sales_data[self.sales_data['year'] == year]

        total_revenue = year_data['price'].sum()
        total_orders = year_data['order_id'].nunique()
        avg_order_value = year_data.groupby('order_id')['price'].sum().mean()

        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'average_order_value': avg_order_value
        }

    def calculate_revenue_growth(self, current_year: int, previous_year: int) -> float:
        """Calculate year-over-year revenue growth rate.

        Args:
            current_year: Current year for analysis
            previous_year: Previous year for comparison

        Returns:
            Growth rate as percentage
        """
        current_revenue = self.sales_data[self.sales_data['year'] == current_year]['price'].sum()
        previous_revenue = self.sales_data[self.sales_data['year'] == previous_year]['price'].sum()

        if previous_revenue == 0:
            return 0.0

        return ((current_revenue - previous_revenue) / previous_revenue) * 100

    def calculate_monthly_growth(self, year: int) -> pd.Series:
        """Calculate month-over-month growth rate within a year.

        Args:
            year: Year to analyze

        Returns:
            Series with monthly growth rates
        """
        year_data = self.sales_data[self.sales_data['year'] == year]
        monthly_revenue = year_data.groupby('month')['price'].sum()
        return monthly_revenue.pct_change() * 100

    def calculate_average_monthly_growth(self, year: int) -> float:
        """Calculate average month-over-month growth for a year.

        Args:
            year: Year to analyze

        Returns:
            Average monthly growth rate as percentage
        """
        monthly_growth = self.calculate_monthly_growth(year)
        return monthly_growth.mean()

    def calculate_order_metrics(self, year: int) -> Dict[str, Any]:
        """Calculate order-related metrics.

        Args:
            year: Year to analyze

        Returns:
            Dictionary containing order metrics
        """
        year_data = self.sales_data[self.sales_data['year'] == year]

        total_orders = year_data['order_id'].nunique()
        avg_items_per_order = year_data.groupby('order_id').size().mean()

        return {
            'total_orders': total_orders,
            'avg_items_per_order': avg_items_per_order
        }

    def calculate_satisfaction_metrics(
        self,
        sales_data_with_reviews: pd.DataFrame
    ) -> Dict[str, Any]:
        """Calculate customer satisfaction metrics.

        Args:
            sales_data_with_reviews: Sales data merged with review scores

        Returns:
            Dictionary containing satisfaction metrics
        """
        avg_review_score = sales_data_with_reviews['review_score'].mean()
        high_satisfaction = (sales_data_with_reviews['review_score'] >= 4).sum() / len(sales_data_with_reviews) * 100

        return {
            'average_review_score': avg_review_score,
            'high_satisfaction_percent': high_satisfaction
        }

    def calculate_delivery_metrics(
        self,
        sales_data_with_reviews: pd.DataFrame
    ) -> Dict[str, Any]:
        """Calculate delivery-related metrics.

        Args:
            sales_data_with_reviews: Sales data with delivery speed calculated

        Returns:
            Dictionary containing delivery metrics
        """
        avg_delivery_days = sales_data_with_reviews['delivery_speed'].mean()
        fast_delivery_percent = (sales_data_with_reviews['delivery_speed'] <= 3).sum() / len(sales_data_with_reviews) * 100

        return {
            'average_delivery_days': avg_delivery_days,
            'fast_delivery_percent': fast_delivery_percent
        }

    def get_monthly_revenue(self, year: int) -> pd.DataFrame:
        """Get monthly revenue breakdown for a year.

        Args:
            year: Year to analyze

        Returns:
            DataFrame with month and revenue columns
        """
        year_data = self.sales_data[self.sales_data['year'] == year]
        monthly_revenue = year_data.groupby('month')['price'].sum().reset_index()
        monthly_revenue.columns = ['month', 'revenue']
        return monthly_revenue

    def get_category_performance(self, sales_data_with_categories: pd.DataFrame) -> pd.DataFrame:
        """Get revenue by product category.

        Args:
            sales_data_with_categories: Sales data merged with product categories

        Returns:
            DataFrame with category and revenue, sorted descending
        """
        return sales_data_with_categories.sort_values('price', ascending=False).reset_index(drop=True)

    def categorize_delivery_speed(self, days: int) -> str:
        """Categorize delivery speed into ranges.

        Args:
            days: Number of delivery days

        Returns:
            Delivery time category string
        """
        if days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'

    def get_delivery_satisfaction_analysis(
        self,
        sales_data_with_reviews: pd.DataFrame
    ) -> pd.DataFrame:
        """Analyze satisfaction by delivery time category.

        Args:
            sales_data_with_reviews: Sales data with delivery speed and review scores

        Returns:
            DataFrame with delivery category and average satisfaction
        """
        data = sales_data_with_reviews.copy()
        data['delivery_category'] = data['delivery_speed'].apply(self.categorize_delivery_speed)

        return data.groupby('delivery_category')['review_score'].mean().reset_index()

    def generate_comprehensive_report(
        self,
        current_year: int,
        previous_year: int,
        sales_data_with_reviews: pd.DataFrame
    ) -> Dict[str, Any]:
        """Generate comprehensive business report.

        Args:
            current_year: Current year for analysis
            previous_year: Previous year for comparison
            sales_data_with_reviews: Sales data merged with reviews

        Returns:
            Dictionary containing all calculated metrics
        """
        return {
            'current_year': current_year,
            'previous_year': previous_year,
            'current_year_metrics': self.calculate_revenue_metrics(current_year),
            'previous_year_metrics': self.calculate_revenue_metrics(previous_year),
            'revenue_growth': self.calculate_revenue_growth(current_year, previous_year),
            'order_metrics': self.calculate_order_metrics(current_year),
            'satisfaction_metrics': self.calculate_satisfaction_metrics(sales_data_with_reviews),
            'delivery_metrics': self.calculate_delivery_metrics(sales_data_with_reviews),
            'monthly_growth': self.calculate_average_monthly_growth(current_year)
        }


class MetricsVisualizer:
    """Create visualizations for business metrics."""

    def __init__(self, metrics_calculator: BusinessMetricsCalculator):
        """Initialize visualizer with metrics calculator.

        Args:
            metrics_calculator: BusinessMetricsCalculator instance
        """
        self.calc = metrics_calculator

    def plot_revenue_trend(
        self,
        current_year: int,
        previous_year: int,
        title: str = 'Monthly Revenue Trend'
    ):
        """Create revenue trend comparison chart.

        Args:
            current_year: Current year
            previous_year: Previous year
            title: Chart title

        Returns:
            Plotly figure object
        """
        current_data = self.calc.get_monthly_revenue(current_year)
        previous_data = self.calc.get_monthly_revenue(previous_year)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=current_data['month'],
            y=current_data['revenue'],
            mode='lines+markers',
            name=str(current_year),
            line=dict(color='#1f77b4', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=previous_data['month'],
            y=previous_data['revenue'],
            mode='lines+markers',
            name=str(previous_year),
            line=dict(color='#ff7f0e', width=2)
        ))

        fig.update_layout(
            title=title,
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )

        return fig

    def plot_category_performance(
        self,
        category_data: pd.DataFrame,
        title: str = 'Revenue by Product Category',
        top_n: int = 10
    ):
        """Create category performance bar chart.

        Args:
            category_data: Category performance data
            title: Chart title
            top_n: Number of top categories to display

        Returns:
            Plotly figure object
        """
        data = category_data.head(top_n).copy()
        data.columns = ['category', 'revenue']

        fig = px.bar(
            data,
            x='revenue',
            y='category',
            orientation='h',
            title=title,
            labels={'revenue': 'Revenue ($)', 'category': 'Product Category'},
            color='revenue',
            color_continuous_scale='Blues'
        )

        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig

    def plot_geographic_distribution(
        self,
        state_data: pd.DataFrame,
        title: str = 'Revenue by State'
    ):
        """Create geographic heatmap.

        Args:
            state_data: State revenue data
            title: Chart title

        Returns:
            Plotly figure object
        """
        state_data.columns = ['state', 'revenue']

        fig = px.choropleth(
            state_data,
            locations='state',
            color='revenue',
            locationmode='USA-states',
            scope='usa',
            title=title,
            color_continuous_scale='Reds',
            labels={'revenue': 'Revenue ($)'}
        )

        fig.update_layout(
            height=500,
            template='plotly_white'
        )

        return fig

    def plot_satisfaction_distribution(
        self,
        sales_data_with_reviews: pd.DataFrame,
        title: str = 'Customer Satisfaction Distribution'
    ):
        """Create satisfaction score distribution chart.

        Args:
            sales_data_with_reviews: Sales data with review scores
            title: Chart title

        Returns:
            Plotly figure object
        """
        satisfaction = sales_data_with_reviews['review_score'].value_counts().sort_index()
        satisfaction_pct = (satisfaction / satisfaction.sum() * 100)

        fig = px.bar(
            x=satisfaction_pct.index,
            y=satisfaction_pct.values,
            title=title,
            labels={'x': 'Review Score', 'y': 'Percentage (%)'},
            color=satisfaction_pct.values,
            color_continuous_scale='RdYlGn'
        )

        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig

    def plot_delivery_satisfaction_analysis(
        self,
        delivery_analysis: pd.DataFrame,
        title: str = 'Average Satisfaction by Delivery Speed'
    ):
        """Create delivery speed vs satisfaction chart.

        Args:
            delivery_analysis: Delivery analysis data
            title: Chart title

        Returns:
            Plotly figure object
        """
        delivery_analysis.columns = ['delivery_category', 'avg_score']

        fig = px.bar(
            delivery_analysis,
            x='delivery_category',
            y='avg_score',
            title=title,
            labels={'delivery_category': 'Delivery Speed', 'avg_score': 'Average Review Score'},
            color='avg_score',
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig


def format_currency(value: float) -> str:
    """Format numeric value as currency string.

    Args:
        value: Numeric value to format

    Returns:
        Formatted currency string
    """
    if value >= 1_000_000:
        return f'${value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'${value / 1_000:.0f}K'
    else:
        return f'${value:.2f}'


def print_metrics_report(report: Dict[str, Any]) -> None:
    """Print formatted business metrics report.

    Args:
        report: Metrics report dictionary from generate_comprehensive_report
    """
    year = report['current_year']

    print(f"\nBUSINESS METRICS SUMMARY - {year}")
    print("=" * 60)

    print(f"\nREVENUE PERFORMANCE:")
    print(f"  Total Revenue: {format_currency(report['current_year_metrics']['total_revenue'])}")
    print(f"  Total Orders: {report['order_metrics']['total_orders']:,}")
    print(f"  Average Order Value: {format_currency(report['current_year_metrics']['average_order_value'])}")
    print(f"  Revenue Growth: {report['revenue_growth']:+.1f}%")
    print(f"  Monthly Growth Trend: {report['monthly_growth']:+.2f}%")

    print(f"\nCUSTOMER SATISFACTION:")
    print(f"  Average Review Score: {report['satisfaction_metrics']['average_review_score']:.2f}/5.0")
    print(f"  High Satisfaction (4+): {report['satisfaction_metrics']['high_satisfaction_percent']:.1f}%")

    print(f"\nDELIVERY PERFORMANCE:")
    print(f"  Average Delivery Time: {report['delivery_metrics']['average_delivery_days']:.1f} days")
    print(f"  Fast Delivery (<=3 days): {report['delivery_metrics']['fast_delivery_percent']:.1f}%")

    print("\n" + "=" * 60)
