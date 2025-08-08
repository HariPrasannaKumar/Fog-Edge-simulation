# main.py
# Entry point for running all scenarios and producing outputs:
# - latency_comparison.png
# - task_distribution_comparison.png
# - simulation_results_all.csv
# - simulation_summary.csv

import pandas as pd
from environment import run_simulation
from metrics import (
    generate_comparison_graph,
    generate_task_distribution_graph,
    save_results_csv,
    save_summary_csv,
)

def run_all_scenarios():
    """
    Run three scenarios and collect results:
    1) Edge-only   : all tasks go to edge nodes
    2) Cloud-only  : all tasks go to cloud
    3) Hybrid      : edge first; fallback to cloud when edge is busy
    """
    print("\n🔹 Running Edge-only Scenario")
    edge_only = run_simulation(sim_time=5000, scenario="edge_only")

    print("\n🔹 Running Cloud-only Scenario")
    cloud_only = run_simulation(sim_time=5000, scenario="cloud_only")

    print("\n🔹 Running Hybrid Scenario")
    hybrid = run_simulation(sim_time=5000, scenario="hybrid")

    # Bundle all results into a dictionary keyed by scenario name
    all_results = {
        "Edge-only": edge_only,
        "Cloud-only": cloud_only,
        "Hybrid": hybrid,
    }

    # ---- Graphs (non-blocking) ----
    # Bar chart of average latency per scenario
    generate_comparison_graph(all_results, show=False)

    # Grouped bar chart of task counts per processing node per scenario
    generate_task_distribution_graph(all_results, show=False)

    # ---- CSV outputs ----
    # 1) Raw row-level output (every task from every scenario)
    save_results_csv(all_results, out_path="simulation_results_all.csv")

    # 2) Compact summary (avg latency + task counts per node per scenario)
    save_summary_csv(all_results, out_path="simulation_summary.csv")

    print("✅ Saved:")
    print("   • latency_comparison.png")
    print("   • task_distribution_comparison.png")
    print("   • simulation_results_all.csv")
    print("   • simulation_summary.csv")

if __name__ == "__main__":
    run_all_scenarios()
