import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import sys

def fetch_data():
    url = input("Paste CSV/JSON open data URL (or local path): ").strip()
    if url.startswith("http"):
        # Download
        ext = url.split("?")[0].split(".")[-1]
        try:
            if ext == 'csv':
                df = pd.read_csv(url)
            elif ext == 'json':
                df = pd.read_json(url)
            else:
                print("Unsupported extension; downloading as CSV anyway.")
                df = pd.read_csv(url)
        except Exception as e:
            print(f"Failed to load: {e}")
            sys.exit(1)
    else:
        if url.lower().endswith('csv'):
            df = pd.read_csv(url)
        elif url.lower().endswith('json'):
            df = pd.read_json(url)
        else:
            print("Only CSV/JSON supported.")
            sys.exit(1)
    return df

def etl_pipeline(df):
    while True:
        cmd = input("\nETL command (help for options, done to finish): ").strip().lower()
        if cmd == 'done':
            break
        elif cmd == 'help':
            print("""
Options:
- filter <col> <operator> <value>  (e.g., filter country == US)
- groupby <col> agg <agg_col> <agg_func>  (e.g., groupby year agg population sum)
- sort <col> [asc/desc]
- dropna <col>
- head <N> : see top N rows
- pivot <index> <columns> <values>
""")
        elif cmd.startswith('filter '):
            try:
                _, col, op, val = cmd.split(" ", 3)
                val = val.strip('"').strip("'")
                if op == "==":
                    df = df[df[col] == val]
                elif op == "!=":
                    df = df[df[col] != val]
                elif op in (">", "<", ">=", "<="):
                    df = df.query(f"{col} {op} @val")
                print(f"Filter applied: {col} {op} {val}")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd.startswith('groupby '):
            try:
                _, gcol, _, acol, afunc = cmd.split()
                df = df.groupby(gcol).agg({acol: afunc}).reset_index()
                print(f"Grouped by {gcol}, {afunc} of {acol}")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd.startswith('sort '):
            parts = cmd.split()
            col, order = parts[1], (parts[2] if len(parts) > 2 else 'asc')
            ascending = order == 'asc'
            df = df.sort_values(col, ascending=ascending)
            print(f"Sorted by {col} {order}")
        elif cmd.startswith('dropna '):
            col = cmd.split()[1]
            df = df.dropna(subset=[col])
            print(f"Dropped rows where {col} is NA")
        elif cmd.startswith('pivot '):
            _, idx, coln, valn = cmd.split()
            df = df.pivot_table(index=idx, columns=coln, values=valn)
            print(f"Pivoted: index={idx}, columns={coln}, values={valn}")
        elif cmd.startswith('head '):
            n = int(cmd.split()[1])
            print(df.head(n))
        else:
            print("Unknown or malformed command.")
    return df

def viz(df):
    print("\nColumns:", list(df.columns))
    plot_type = input("Plot type (line/bar/scatter/hist): ").strip()
    y = input("Y column: ").strip()
    x = input("X column (blank=auto): ").strip() or None
    plt.figure(figsize=(9,5))
    if plot_type == "line":
        df.plot(y=y, x=x)
    elif plot_type == "bar":
        df.plot.bar(y=y, x=x)
    elif plot_type == "scatter":
        plt.scatter(df[x], df[y])
    elif plot_type == "hist":
        df[y].hist()
    else:
        print("Unknown plot type.")
        return
    plt.title(f"{y} vs {x}" if x else y)
    plt.tight_layout()
    plt.savefig("etl_plot.png")
    plt.show()
    print("Plot saved as etl_plot.png")

def main():
    print("=== Open Data ETL & Visualization Engine ===")
    df = fetch_data()
    print(f"\nLoaded data with {len(df)} rows, columns:\n{list(df.columns)}")
    df = etl_pipeline(df)
    # Save snapshot
    outname = "etl_result.csv"
    df.to_csv(outname, index=False)
    print(f"\nFinal data saved as {outname} (shape: {df.shape})")
    viz(df)

if __name__ == "__main__":
    print("Dependencies: pandas, matplotlib.")
    main()
