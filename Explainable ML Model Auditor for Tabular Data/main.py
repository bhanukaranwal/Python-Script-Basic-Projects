import pandas as pd
import pickle
import shap
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# --- Utility functions ---
def get_model_and_data():
    csv_path = input("Path to your tabular dataset CSV: ").strip()
    pkl_path = input("Path to your scikit-learn model .pkl file: ").strip()
    if not os.path.exists(csv_path) or not os.path.exists(pkl_path):
        print("Invalid paths. Please check input files.")
        sys.exit(1)
    data = pd.read_csv(csv_path)
    with open(pkl_path, "rb") as f:
        model = pickle.load(f)
    return data, model

def get_rows_to_explain(data):
    print("\nSample rows to choose from:")
    print(data.head())
    idxes = input("Enter comma-separated row indices for local explanation (blank for first row): ").strip()
    if not idxes:
        idxes = [0]
    else:
        idxes = [int(i) for i in idxes.split(",") if i.isdigit()]
    return idxes

def save_shap_summary_html(explainer, shap_values, feature_names):
    shap_html = shap.summary_plot(
        shap_values, features=None, feature_names=feature_names, plot_type="bar", show=False
    )
    plt.savefig("global_shap_summary.png", bbox_inches='tight')
    plt.close()
    with open("shap_report.html", "w", encoding="utf-8") as f:
        f.write(f"""<html><head><title>Explainable ML Auditor</title></head>
        <body>
        <h1>Global Feature Importance (SHAP)</h1>
        <img src="global_shap_summary.png" width="800"><p>See local explanations below.</p>
        </body></html>""")
    print("Saved HTML summary as shap_report.html and summary plot.")

def explain_row_local(model, explainer, row, feature_names, idx):
    shap_values = explainer.shap_values(row)
    plt.figure()
    shap.waterfall_plot(explainer.expected_value, shap_values[0], features=row.iloc[0], feature_names=feature_names, show=False)
    fname = f"local_explain_{idx}.png"
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    print(f"Saved local explanation for row {idx} as {fname}.")

# --- Main Auditing Routine ---
def main():
    print("=== Explainable ML Model Auditor (single-file edition) ===")
    data, model = get_model_and_data()
    X = data.select_dtypes(include=[np.number])
    print(f"Loaded dataset with {X.shape[0]} rows, {X.shape[1]} numeric features.")
    predictions = model.predict(X)
    print(f"\n--- Prediction Step ---\nFirst 5 predictions: {predictions[:5]}")
    feature_names = X.columns.tolist()

    # SHAP explainability
    print("\n--- SHAP Global/Local Explanations ---")
    try:
        explainer = shap.Explainer(model, X)
        global_shap_values = explainer(X)
        # Save summary
        save_shap_summary_html(explainer, global_shap_values.values, feature_names)
        # Local explanation for selected rows
        indices = get_rows_to_explain(data)
        for idx in indices:
            row = X.iloc[[idx]]
            explain_row_local(model, explainer, row, feature_names, idx)
    except Exception as e:
        print(f"SHAP explanation failed: {e}. Try a different model type or environmental setup.")

    # Outlier detection (simple Z-score method)
    print("\n--- Outlier Warning ---")
    zscores = np.abs((X - X.mean()) / X.std())
    outlier_rows = np.where((zscores > 4).any(axis=1))[0]
    if len(outlier_rows) > 0:
        print(f"Data contains potential outlier rows at indices: {outlier_rows.tolist()}")

    print("\nAuditing complete. Check the generated HTML report and PNGs for visual explanations.")

if __name__ == "__main__":
    print("Dependencies required: pandas, numpy, scikit-learn, shap, matplotlib.")
    main()
