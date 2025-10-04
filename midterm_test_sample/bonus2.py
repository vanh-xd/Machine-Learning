import pandas as pd
from typing import List, Tuple


def get_top_n_invoices_in_range(
        df: pd.DataFrame,
        minValue: float,
        maxValue: float,
        n: int,
        invoice_id_col: str = 'OrderID',
        sum_col: str = 'Sum'
) -> List[Tuple[str, float]]:

    filtered_df = df[(df[sum_col] >= minValue) & (df[sum_col] <= maxValue)]

    top_n = filtered_df.nlargest(n, sum_col)

    return list(zip(top_n[invoice_id_col], top_n[sum_col]))

def get_top_n_customers_by_invoice_count(
        df: pd.DataFrame,
        n: int,
        customer_id_col: str = 'CustomerID',
        invoice_id_col: str = 'OrderID'
) -> List[Tuple[str, int]]:

    customer_invoice_count = df.groupby(customer_id_col)[invoice_id_col].count().reset_index()
    customer_invoice_count.columns = [customer_id_col, 'InvoiceCount']

    top_n = customer_invoice_count.nlargest(n, 'InvoiceCount')

    return list(zip(top_n[customer_id_col], top_n['InvoiceCount']))


def get_top_n_customers_by_total_value(
        df: pd.DataFrame,
        n: int,
        customer_id_col: str = 'CustomerID',
        sum_col: str = 'Sum'
) -> List[Tuple[str, float]]:

    customer_total_value = df.groupby(customer_id_col)[sum_col].sum().reset_index()
    customer_total_value.columns = [customer_id_col, 'TotalValue']

    top_n = customer_total_value.nlargest(n, 'TotalValue')

    return list(zip(top_n[customer_id_col], top_n['TotalValue']))
