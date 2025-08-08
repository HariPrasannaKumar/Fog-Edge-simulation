# metrics.py
# Visualization and CSV helpers for the simulation results.

import pandas as pd
import matplotlib.pyplot as plt

def _safe_to_dataframe(results):
    """
    Convert a list[dict] to a DataFrame safely.
    Returns an empty DataFrame if results is empty/None.
    """
    if not results:
        return pd.DataFrame(columns=["task_id", "processed_by", "latency", "type"])
    return pd.DataFrame(results)


def generate_comparison_graph(results_dict, show=False):
    """
    Create a bar chart of average latency for each scenario.

    Parameters
    ----------
    results_dict : dict[str, list[dict]]
        Keys are scenario names, values are lists of task-result dicts.
    show : bool
        If True, display the figure window. Defaults to False (non-blocking).
    """
    avg_latencies = {}
    for scenario_name, results in results_dict.items():
        df = _safe_to_dataframe(results)
        # If there are no rows, store NaN to keep the bar visible
        avg_latencies[scenario_name] = df["latency"].mean() if not df.empty else float("nan")

    # Plot (non-blocking)
    plt.figure(figsize=(8, 5))
    bars = plt.bar(avg_latencies.keys(), avg_latencies.values())
    plt.ylabel("Average Latency (ms)")
    plt.title("Average Latency Comparison by Scenario")
    plt.xticks(rotation=0)

    # Add labels above bars
    for bar in bars:
        h = bar.get_height()
        if pd.notna(h):
            plt.text(bar.get_x() + bar.get_width()/2, h + 5, f"{h:.1f}",
                     ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("latency_comparison.png", dpi=300)
    if show:
        plt.show()
    plt.close()


def generate_task_distribution_graph(results_dict, show=False):
    """
    Create a grouped bar chart of task counts by processing node (Edge1/Edge2/Cloud)
    for each scenario.

    Parameters
    ----------
    results_dict : dict[str, list[dict]]
    show : bool
    """
    # Build a table: rows = processing nodes, columns = scenarios, cells = counts
    task_counts = {}
    for scenario_name, results in results_dict.items():
        df = _safe_to_dataframe(results)
        counts = df["processed_by"].value_counts() if not df.empty else pd.Series(dtype=int)
        task_counts[scenario_name] = counts

    # Combine to a single DataFrame; missing values -> 0
    task_df = pd.DataFrame(task_counts).fillna(0).astype(int)

    # Plot (note: .plot returns an axes; we still manage figure lifecycle below)
    ax = task_df.plot(kind="bar", figsize=(9, 5))
    ax.set_title("Task Distribution by Node for Each Scenario")
    ax.set_xlabel("Processing Node")
    ax.set_ylabel("Number of Tasks")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig("task_distribution_comparison.png", dpi=300)
    if show:
        plt.show()
    plt.close()


def save_results_csv(results_dict, out_path="simulation_results_all.csv"):
    """
    Save all task rows for all scenarios into a single CSV.
    Adds a 'scenario' column so you can filter later in Excel/Pandas.

    Columns:
      scenario, task_id, processed_by, latency, type
    """
    frames = []
    for scenario, results in results_dict.items():
        df = _safe_to_dataframe(results)
        df["scenario"] = scenario
        frames.append(df)

    if frames:
        final_df = pd.concat(frames, ignore_index=True)
    else:
        final_df = pd.DataFrame(columns=["scenario", "task_id", "processed_by", "latency", "type"])

    final_df.to_csv(out_path, index=False)


def save_summary_csv(results_dict, out_path="simulation_summary.csv"):
    """
    Save a compact summary per scenario:
      - average latency
      - counts per processing node (Edge1, Edge2, Cloud)

    Produces a wide CSV like:
      scenario, avg_latency, Edge1, Edge2, Cloud
    """
    rows = []
    all_nodes = set()

    # First pass: gather counts and avg latency
    for scenario, results in results_dict.items():
        df = _safe_to_dataframe(results)
        avg_latency = df["latency"].mean() if not df.empty else float("nan")
        counts = df["processed_by"].value_counts() if not df.empty else pd.Series(dtype=int)

        # Keep track of all node labels to make consistent columns
        all_nodes.update(counts.index.tolist())

        rows.append({
            "scenario": scenario,
            "avg_latency": avg_latency,
            "_counts": counts,  # temporarily store series
        })

    # Second pass: flatten counts into dedicated columns
    all_nodes = sorted(all_nodes)  # stable column order
    flat_rows = []
    for row in rows:
        flat = {"scenario": row["scenario"], "avg_latency": row["avg_latency"]}
        counts = row["_counts"]
        for node in all_nodes:
            flat[node] = int(counts.get(node, 0))
        flat_rows.append(flat)

    summary_df = pd.DataFrame(flat_rows, columns=["scenario", "avg_latency"] + all_nodes)
    summary_df.to_csv(out_path, index=False)
