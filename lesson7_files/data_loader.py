"""
Data loading and preprocessing module for e-commerce analysis.

This module provides utilities for loading, cleaning, and transforming
raw e-commerce datasets into analysis-ready formats.
"""

import pandas as pd
from typing import Dict, Optional, Tuple


class EcommerceDataLoader:
    """Load and process e-commerce datasets."""

    def __init__(self, data_path: str = 'ecommerce_data/'):
        """Initialize data loader with path to data files.

        Args:
            data_path: Path to directory containing CSV files
        """
        self.data_path = data_path
        self.orders = None
        self.order_items = None
        self.products = None
        self.customers = None
        self.reviews = None

    def load_raw_data(self) -> None:
        """Load all raw CSV files into memory."""
        self.orders = pd.read_csv(f'{self.data_path}orders_dataset.csv')
        self.order_items = pd.read_csv(f'{self.data_path}order_items_dataset.csv')
        self.products = pd.read_csv(f'{self.data_path}products_dataset.csv')
        self.customers = pd.read_csv(f'{self.data_path}customers_dataset.csv')
        self.reviews = pd.read_csv(f'{self.data_path}order_reviews_dataset.csv')

    def _prepare_orders(self) -> pd.DataFrame:
        """Prepare orders data with datetime columns and year field."""
        df = self.orders.copy()
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
        df['year'] = df['order_purchase_timestamp'].dt.year
        df['month'] = df['order_purchase_timestamp'].dt.month
        return df

    def _prepare_order_items(self) -> pd.DataFrame:
        """Prepare order items data."""
        return self.order_items.copy()

    def _prepare_products(self) -> pd.DataFrame:
        """Prepare products data."""
        return self.products.copy()

    def _prepare_customers(self) -> pd.DataFrame:
        """Prepare customers data."""
        return self.customers.copy()

    def _prepare_reviews(self) -> pd.DataFrame:
        """Prepare reviews data with datetime conversion."""
        df = self.reviews.copy()
        df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
        return df

    def process_all_data(self) -> Dict[str, pd.DataFrame]:
        """Process all datasets and return dictionary of cleaned data."""
        return {
            'orders': self._prepare_orders(),
            'order_items': self._prepare_order_items(),
            'products': self._prepare_products(),
            'customers': self._prepare_customers(),
            'reviews': self._prepare_reviews()
        }

    def create_sales_dataset(
        self,
        year_filter: Optional[int] = None,
        month_filter: Optional[int] = None,
        status_filter: str = 'delivered'
    ) -> pd.DataFrame:
        """Create merged sales dataset with filtering.

        Args:
            year_filter: Filter by specific year (None for all years)
            month_filter: Filter by specific month (None for all months)
            status_filter: Filter by order status (default: 'delivered')

        Returns:
            Merged and filtered sales dataset
        """
        orders = self._prepare_orders()
        order_items = self._prepare_order_items()

        sales_data = pd.merge(
            left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
            right=orders[['order_id', 'order_status', 'order_purchase_timestamp',
                         'order_delivered_customer_date', 'year', 'month']],
            on='order_id'
        )

        sales_data = sales_data[sales_data['order_status'] == status_filter]

        if year_filter is not None:
            sales_data = sales_data[sales_data['year'] == year_filter]

        if month_filter is not None:
            sales_data = sales_data[sales_data['month'] == month_filter]

        return sales_data

    def create_geographic_dataset(
        self,
        sales_data: pd.DataFrame,
        year_filter: Optional[int] = None
    ) -> pd.DataFrame:
        """Create geographic dataset with sales by state.

        Args:
            sales_data: Sales dataset (filtered as needed)
            year_filter: Filter by specific year

        Returns:
            Dataset with revenue by state
        """
        orders = self._prepare_orders()
        customers = self._prepare_customers()

        sales_with_customers = pd.merge(
            left=sales_data[['order_id', 'price']],
            right=orders[['order_id', 'customer_id', 'year']],
            on='order_id'
        )

        if year_filter is not None:
            sales_with_customers = sales_with_customers[sales_with_customers['year'] == year_filter]

        sales_states = pd.merge(
            left=sales_with_customers,
            right=customers[['customer_id', 'customer_state']],
            on='customer_id'
        )

        return sales_states.groupby('customer_state')['price'].sum().reset_index()

    def create_product_category_dataset(
        self,
        sales_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Create product category performance dataset.

        Args:
            sales_data: Sales dataset (filtered as needed)

        Returns:
            Dataset with revenue by product category
        """
        products = self._prepare_products()

        sales_with_products = pd.merge(
            left=products[['product_id', 'product_category_name']],
            right=sales_data[['product_id', 'price']],
            on='product_id'
        )

        return sales_with_products.groupby('product_category_name')['price'].sum().sort_values(ascending=False).reset_index()

    def create_delivery_review_dataset(
        self,
        sales_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Create dataset for delivery time vs review score analysis.

        Args:
            sales_data: Sales dataset (filtered as needed)

        Returns:
            Dataset with delivery speed and review scores
        """
        reviews = self._prepare_reviews()

        sales_with_reviews = pd.merge(
            left=sales_data[['order_id', 'order_purchase_timestamp', 'order_delivered_customer_date']],
            right=reviews[['order_id', 'review_score']],
            on='order_id'
        ).drop_duplicates(subset=['order_id'])

        sales_with_reviews['delivery_speed'] = (
            sales_with_reviews['order_delivered_customer_date'] -
            sales_with_reviews['order_purchase_timestamp']
        ).dt.days

        return sales_with_reviews[['order_id', 'delivery_speed', 'review_score']]


def load_and_process_data(data_path: str = 'ecommerce_data/') -> Tuple[EcommerceDataLoader, Dict[str, pd.DataFrame]]:
    """Convenience function to load and process all data.

    Args:
        data_path: Path to data directory

    Returns:
        Tuple of (loader instance, processed data dictionary)
    """
    loader = EcommerceDataLoader(data_path)
    loader.load_raw_data()
    processed_data = loader.process_all_data()
    return loader, processed_data
