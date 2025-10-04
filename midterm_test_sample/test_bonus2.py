import pandas as pd
from bonus.midterm_test_sample.bonus2 import (
    get_top_n_invoices_in_range,
    get_top_n_customers_by_invoice_count,
    get_top_n_customers_by_total_value
)

data = {
    'OrderID': ['INV001', 'INV002', 'INV003', 'INV004', 'INV005', 'INV006', 'INV007', 'INV008'],
    'CustomerID': ['CUST001', 'CUST002', 'CUST001', 'CUST003', 'CUST002', 'CUST001', 'CUST004', 'CUST002'],
    'Sum': [500, 800, 900, 1200, 650, 750, 300, 950]
}
df = pd.DataFrame(data)

print("Sample DataFrame:")
print(df)
print("\n" + "=" * 60 + "\n")

print("Function 1: TOP 3 invoices with value between 600 and 1000")
result1 = get_top_n_invoices_in_range(df, minValue=600, maxValue=1000, n=3)
print(result1)
print("\n" + "=" * 60 + "\n")

print("Function 2: TOP 3 customers with most invoices")
result2 = get_top_n_customers_by_invoice_count(df, n=3)
print(result2)
print("\n" + "=" * 60 + "\n")

print("Function 3: TOP 3 customers with highest total invoice value")
result3 = get_top_n_customers_by_total_value(df, n=3)
print(result3)
print("\n" + "=" * 60 + "\n")

print("Additional Examples:")
print("\nTOP 2 invoices between 500-800:")
print(get_top_n_invoices_in_range(df, 500, 800, 2))

print("\nTOP 2 customers by invoice count:")
print(get_top_n_customers_by_invoice_count(df, 2))

print("\nTOP 2 customers by total value:")
print(get_top_n_customers_by_total_value(df, 2))

print("\n" + "=" * 60)

try:
    min_input = input("Enter minimum invoice value (or press Enter to skip): ").strip()

    if min_input:
        min_value = float(min_input)

        max_input = input("Enter maximum invoice value: ").strip()
        max_value = float(max_input)

        n_input = input("Enter number of top invoices to display (default 5): ").strip()
        n_value = int(n_input) if n_input else 5

        if min_value > max_value:
            print("\nError: Minimum value cannot be greater than maximum value!")
        elif n_value <= 0:
            print("\nError: Number of invoices must be greater than 0!")
        else:
            print(f"\nSearching for TOP {n_value} invoices with value between {min_value} and {max_value}...")
            user_result = get_top_n_invoices_in_range(df, min_value, max_value, n_value)

            if user_result:
                print(f"\nFound {len(user_result)} invoice(s):")
                for idx, (invoice_id, value) in enumerate(user_result, 1):
                    print(f"  {idx}. {invoice_id}: ${value:,.2f}")
            else:
                print("\nNo invoices found in the specified range.")
    else:
        print("Skipping interactive mode.\n")

except ValueError:
    print("\nError: Please enter valid numeric values!")
except KeyboardInterrupt:
    print("\n\nInteractive mode cancelled by user.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
