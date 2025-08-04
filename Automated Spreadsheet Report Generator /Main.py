import pandas as pd

def spreadsheet_report_generator():
    print("\nGenerating a summary report from example sales data")

    # Example data—replace with pd.read_csv("yourfile.csv") for real workflow
    data = {
        'Region': ['East', 'West', 'East', 'North', 'West', 'North', 'East'],
        'Sales': [200, 300, 250, 400, 150, 350, 50],
        'Profit': [50, 80, 45, 110, 30, 90, 10],
        'Orders': [20, 35, 23, 40, 18, 34, 7]
    }
    df = pd.DataFrame(data)
    print("Sample data:")
    print(df)

    # Group by Region, aggregate Sales, Profit, and Orders
    report = df.groupby('Region').agg({
        'Sales': ['sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Orders': ['sum', 'mean']
    })
    report.columns = ['_'.join(col) for col in report.columns]
    report.reset_index(inplace=True)
    print("\nGenerated Report:")
    print(report)

    # Save to CSV
    output_file = 'sales_report.csv'
    report.to_csv(output_file, index=False)
    print(f"\nReport saved to {output_file}")

if __name__ == '__main__':
    spreadsheet_report_generator()
