# environment.py

import simpy
from models import Task, EdgeNode, CloudNode

def task_generator(env, edge_nodes, cloud, results):
    """
    Generates tasks periodically and sends them to edge nodes if available.
    Falls back to cloud if all edge nodes are busy or not available.
    """
    task_id = 0
    while True:
        yield env.timeout(50)  # Generate a new task every 50ms

        task = Task(id=task_id, size=1000, created=env.now)
        print(f"[{env.now} ms] Task {task_id} created")

        available_edges = [e for e in edge_nodes if e.can_process()]
        if available_edges:
            # Choose the edge node with the least load
            chosen_edge = min(available_edges, key=lambda e: e.load)
            yield env.process(chosen_edge.process(task, env, results))
        else:
            # All edge nodes busy or not available; send to cloud
            print(f"[{env.now} ms] All edges busy — Task {task_id} sent to cloud")
            yield env.process(cloud.process(task, env, results))

        task_id += 1


def run_simulation(sim_time=5000, scenario="hybrid"):
    """
    Run a simulation for a given time and scenario.
    Scenarios:
    - "edge_only": only edge nodes process tasks
    - "cloud_only": only cloud processes tasks
    - "hybrid": use edge first, fallback to cloud
    """
    env = simpy.Environment()
    results = []

    if scenario == "edge_only":
        edge1 = EdgeNode("Edge1", capacity=1)
        edge2 = EdgeNode("Edge2", capacity=1)
        cloud = CloudNode("Cloud", delay=300)  # cloud not used, but needed for fallback param
        edge_nodes = [edge1, edge2]

    elif scenario == "cloud_only":
        edge_nodes = []  # No edge processing available
        cloud = CloudNode("Cloud", delay=300)

    else:  # hybrid scenario
        edge1 = EdgeNode("Edge1", capacity=1)
        edge2 = EdgeNode("Edge2", capacity=1)
        cloud = CloudNode("Cloud", delay=300)
        edge_nodes = [edge1, edge2]

    # Start task generation
    env.process(task_generator(env, edge_nodes, cloud, results))
    env.run(until=sim_time)

    return results
