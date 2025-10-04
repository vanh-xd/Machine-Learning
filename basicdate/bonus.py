import pandas as pd


def filter_invoices(df):
    # Get user input for min and max values
    minValue = int(input("Enter the minimum Sum value: "))
    maxValue = int(input("Enter the maximum Sum value: "))

    # Get user input for sorting type
    sort_choice = input("Choose sort order (asc/desc): ").strip().lower()
    if sort_choice == "asc":
        SortType = True
    elif sort_choice == "desc":
        SortType = False
    else:
        print("Invalid choice! Defaulting to ascending.")
        SortType = True

    # Filter rows within the range
    filtered = df[(df['Sum'] >= minValue) & (df['Sum'] <= maxValue)]

    # Sort based on SortType
    filtered = filtered.sort_values(by="Sum", ascending=SortType)

    # Return DataFrame with only OrderID and Sum
    return filtered[['OrderID', 'Sum']].reset_index(drop=True)


# Example DataFrame
data = {
    "OrderID": ["OrderID1", "OrderID2", "OrderID3"],
    "Sum": [500, 800, 900]
}
df = pd.DataFrame(data)

# Run function
result = filter_invoices(df)
print("\nFiltered and Sorted Invoices:")
print(result)
