# main.py

from environment import run_simulation
from metrics import generate_comparison_graph

def run_all_scenarios():
    """
    Run three different scenarios:
    1. Edge-only: All tasks processed by edge nodes.
    2. Cloud-only: All tasks processed by the cloud.
    3. Hybrid: Tasks are processed by edge nodes if available, else fallback to cloud.
    """
    print("\n🔹 Running Edge-only Scenario")
    edge_only_results = run_simulation(sim_time=5000, scenario="edge_only")

    print("\n🔹 Running Cloud-only Scenario")
    cloud_only_results = run_simulation(sim_time=5000, scenario="cloud_only")

    print("\n🔹 Running Hybrid Scenario")
    hybrid_results = run_simulation(sim_time=5000, scenario="hybrid")

    # Combine results for comparison
    all_results = {
        "Edge-only": edge_only_results,
        "Cloud-only": cloud_only_results,
        "Hybrid": hybrid_results
    }

    # Generate bar graph for comparison
    generate_comparison_graph(all_results)

if __name__ == "__main__":
    run_all_scenarios()
