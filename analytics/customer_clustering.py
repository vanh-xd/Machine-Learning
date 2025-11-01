import os
import sys
import math
import numpy as np
import pandas as pd

# Allow importing Connector from sibling package
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from connectors.connector import Connector


def _zscore_standardize(X: np.ndarray) -> np.ndarray:
    means = X.mean(axis=0)
    stds = X.std(axis=0)
    stds_safe = np.where(stds == 0, 1.0, stds)
    return (X - means) / stds_safe


def _kmeans_numpy(X: np.ndarray, k: int, max_iters: int = 100, random_state: int | None = 42):
    if random_state is not None:
        rng = np.random.default_rng(random_state)
    else:
        rng = np.random.default_rng()

    n_samples = X.shape[0]
    if k <= 0 or k > n_samples:
        raise ValueError(f"Invalid k={k}. Must be between 1 and number of samples {n_samples}.")

    # Initialize centroids by sampling k unique points
    indices = rng.choice(n_samples, size=k, replace=False)
    centroids = X[indices].copy()

    labels = np.zeros(n_samples, dtype=int)

    for _ in range(max_iters):
        # Assign step
        # Compute distances efficiently: (n_samples, k)
        # Using broadcasting for Euclidean distance
        distances = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        new_labels = np.argmin(distances, axis=1)

        # Check convergence
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels

        # Update step: recompute centroids as mean of assigned points
        for ci in range(k):
            mask = labels == ci
            if not np.any(mask):
                # If a cluster lost all points, re-seed it randomly
                centroids[ci] = X[rng.integers(0, n_samples)]
            else:
                centroids[ci] = X[mask].mean(axis=0)

    return labels, centroids


def fetch_customers_df(connector: Connector) -> pd.DataFrame:
    # Use lowercase table name to align with existing tests and schema
    sql = "SELECT * FROM customer"
    df = connector.queryDataset(sql)
    if df is None or df.empty:
        raise RuntimeError("No customers found or query failed. Ensure the 'customer' table exists and has rows in 'salesdatabase'.")
    return df


def get_customers_by_cluster(k: int = 3, feature_cols: list[str] | None = None, random_state: int | None = 42):
    """
    Returns a tuple (clusters_map, full_df_with_cluster) where:
    - clusters_map: dict[int, pd.DataFrame] mapping cluster index -> customer rows (all columns) belonging to that cluster
    - full_df_with_cluster: original DataFrame with an added 'cluster' column
    """
    # Connect to the 'salesdatabase' schema as requested
    connector = Connector(database="salesdatabase")
    conn = connector.connect()
    try:
        df = fetch_customers_df(connector)

        # Select numeric features (auto) if feature_cols not provided
        if feature_cols is None:
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.shape[1] == 0:
                raise RuntimeError("Customer table has no numeric columns for clustering.")
            X = numeric_df.to_numpy(dtype=float)
            used_cols = list(numeric_df.columns)
        else:
            # Validate provided columns
            for col in feature_cols:
                if col not in df.columns:
                    raise KeyError(f"Feature column '{col}' not found in Customer table.")
            X = df[feature_cols].select_dtypes(include=[np.number]).to_numpy(dtype=float)
            used_cols = list(feature_cols)
            if X.shape[1] == 0:
                raise RuntimeError("Selected feature columns are not numeric or empty.")

        # Standardize
        X_std = _zscore_standardize(X)

        # KMeans
        labels, _ = _kmeans_numpy(X_std, k=k, max_iters=100, random_state=random_state)

        # Attach cluster labels to full DF
        df_with_cluster = df.copy()
        df_with_cluster['cluster'] = labels

        # Build mapping
        clusters_map: dict[int, pd.DataFrame] = {}
        for ci in range(k):
            clusters_map[ci] = df_with_cluster[df_with_cluster['cluster'] == ci].reset_index(drop=True)

        return clusters_map, df_with_cluster, used_cols
    finally:
        connector.disConnect()


def display_clusters_console(clusters_map: dict[int, pd.DataFrame]):
    for ci, cdf in clusters_map.items():
        print(f"\n=== Cluster {ci} ({len(cdf)} customers) ===")
        # Display all details without the pandas index
        print(cdf.to_string(index=False))


def render_clusters_html(clusters_map: dict[int, pd.DataFrame], out_path: str, title: str):
    # Build a simple HTML page with tables per cluster
    parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"<meta charset='utf-8'><title>{title}</title>",
        "<style>body{font-family:Arial, sans-serif;margin:20px;} h2{margin-top:30px;} table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ccc;padding:6px;text-align:left;} thead{background:#f2f2f2;}</style>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
    ]

    for ci, cdf in clusters_map.items():
        parts.append(f"<h2>Cluster {ci} ({len(cdf)} customers)</h2>")
        parts.append(cdf.to_html(index=False, border=0))

    parts.append("</body>")
    parts.append("</html>")

    html = "\n".join(parts)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def run_scenarios():
    # Scenario A: k=3 on all numeric features
    clusters_map_a, df_a, used_cols_a = get_customers_by_cluster(k=3)
    print("\n[Scenario A] k=3, features:", used_cols_a)
    display_clusters_console(clusters_map_a)

    # HTML output A
    out_a = os.path.join(PROJECT_ROOT, 'ui', 'clusters_k3.html')
    render_clusters_html(clusters_map_a, out_a, title="Customer Clusters (k=3)")
    print(f"\nHTML written to: {out_a}")

    # Scenario B: k=5 on all numeric features
    clusters_map_b, df_b, used_cols_b = get_customers_by_cluster(k=5)
    print("\n[Scenario B] k=5, features:", used_cols_b)
    display_clusters_console(clusters_map_b)

    # HTML output B
    out_b = os.path.join(PROJECT_ROOT, 'ui', 'clusters_k5.html')
    render_clusters_html(clusters_map_b, out_b, title="Customer Clusters (k=5)")
    print(f"\nHTML written to: {out_b}")


if __name__ == "__main__":
    # Allow optional CLI args: --k <int>
    # If provided, run single scenario with that k, else run the default scenarios
    import argparse
    parser = argparse.ArgumentParser(description="Customer clustering and outputs")
    parser.add_argument("--k", type=int, default=None, help="Number of clusters to run a single scenario")
    args = parser.parse_args()

    if args.k is not None:
        clusters_map, df, used = get_customers_by_cluster(k=args.k)
        print(f"[Single Scenario] k={args.k}, features: {used}")
        display_clusters_console(clusters_map)
        out_single = os.path.join(PROJECT_ROOT, 'ui', f'clusters_k{args.k}.html')
        render_clusters_html(clusters_map, out_single, title=f"Customer Clusters (k={args.k})")
        print(f"HTML written to: {out_single}")
    else:
        run_scenarios()