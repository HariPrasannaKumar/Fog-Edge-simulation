# models.py

class Task:
    """
    Represents a computational task to be processed.
    """
    def __init__(self, id, size, created):
        self.id = id
        self.size = size
        self.created = created


class EdgeNode:
    """
    Simulates an edge node with limited processing capacity.
    """
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.busy = 0  # Tracks how many tasks are currently being processed
        self.load = 0  # Tracks how many total tasks have been assigned

    def can_process(self):
        # Checks if the edge node has available capacity
        return self.busy < self.capacity

    def process(self, task, env, results):
        """
        Processes a task at the edge node with fixed delay.
        """
        self.busy += 1
        self.load += 1
        edge_time = 200  # fixed processing time in ms

        print(f"[{env.now} ms] {self.name} started processing Task {task.id}")
        yield env.timeout(edge_time)
        print(f"[{env.now} ms] {self.name} completed Task {task.id}")

        # Save result with latency
        results.append({
            "task_id": task.id,
            "processed_by": self.name,
            "latency": env.now - task.created,
            "type": "Partial (70%)"
        })

        self.busy -= 1


class CloudNode:
    """
    Simulates a cloud node with constant delay and unlimited capacity.
    """
    def __init__(self, name, delay):
        self.name = name
        self.delay = delay  # Fixed delay in ms

    def process(self, task, env, results):
        """
        Processes a task in the cloud.
        """
        print(f"[{env.now} ms] {self.name} started processing Task {task.id}")
        yield env.timeout(self.delay)
        print(f"[{env.now} ms] {self.name} completed Task {task.id}")

        # Save result with full processing label
        results.append({
            "task_id": task.id,
            "processed_by": self.name,
            "latency": env.now - task.created,
            "type": "Full (100%)"
        })
