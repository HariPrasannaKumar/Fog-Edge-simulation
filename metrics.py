# metrics.py

import pandas as pd
import matplotlib.pyplot as plt

def generate_comparison_graph(results_dict):
    """
    Plots a bar chart showing average latency across all simulation scenarios.
    """
    avg_latencies = {}

    for scenario_name, results in results_dict.items():
        df = pd.DataFrame(results)
        avg_latency = df["latency"].mean()
        avg_latencies[scenario_name] = avg_latency

    # Create bar graph
    plt.figure(figsize=(8, 5))
    bars = plt.bar(avg_latencies.keys(), avg_latencies.values(), color='skyblue')
    plt.ylabel("Average Latency (ms)")
    plt.title("Average Latency Comparison by Scenario")

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 5, f'{height:.1f}', ha='center', va='bottom')

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("latency_comparison.png")
    plt.show()


def generate_task_distribution_graph(results_dict):
    """
    Plots a grouped bar chart showing number of tasks processed by each node per scenario.
    """
    task_counts = {}

    for scenario_name, results in results_dict.items():
        df = pd.DataFrame(results)
        count_by_node = df["processed_by"].value_counts()
        task_counts[scenario_name] = count_by_node

    # Combine all into a DataFrame
    task_df = pd.DataFrame(task_counts).fillna(0).astype(int)

    # Plot as grouped bar chart
    task_df.plot(kind='bar', figsize=(8, 5))
    plt.title("Task Distribution by Node for Each Scenario")
    plt.xlabel("Processing Node")
    plt.ylabel("Number of Tasks")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("task_distribution_comparison.png")
    plt.show()
