import pandas as pd


def filter_and_sort_invoices(df, minValue, maxValue, SortType=True):
    filtered_df = df[(df['Sum'] >= minValue) & (df['Sum'] <= maxValue)]
    sorted_df = filtered_df.sort_values(by='Sum', ascending=SortType)
    result = list(zip(sorted_df['OrderID'], sorted_df['Sum']))
    return result

if __name__ == "__main__":
    data = {
        'OrderID': ['OrderID1', 'OrderID2', 'OrderID3'],
        'Sum': [500, 800, 900]
    }
    df = pd.DataFrame(data)

    print("Original DataFrame:")
    print(df)
    print("\n" + "=" * 50 + "\n")

    result_asc = filter_and_sort_invoices(df, minValue=500, maxValue=900, SortType=True)
    print("SortType=True (Ascending):")
    for order_id, sum_value in result_asc:
        print(f"{order_id}: {sum_value}")

    print("\n" + "=" * 50 + "\n")

    result_desc = filter_and_sort_invoices(df, minValue=500, maxValue=900, SortType=False)
    print("SortType=False (Descending):")
    for order_id, sum_value in result_desc:
        print(f"{order_id}: {sum_value}")

    print("\n" + "=" * 50 + "\n")

    result_filtered = filter_and_sort_invoices(df, minValue=600, maxValue=900, SortType=True)
    print("Filtered (600-900) with SortType=True:")
    for order_id, sum_value in result_filtered:
        print(f"{order_id}: {sum_value}")
