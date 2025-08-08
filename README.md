Fog and Edge Computing Simulation This project simulates task offloading in Industrial IoT scenarios using Fog (Edge) and Cloud computing environments. It is inspired by the 2024 paper:

X. Jin et al., Latency-aware Multi-Server Partial Edge Computing Task Offloading in Industrial IoT, 2024.

📌 Overview The simulator models three scenarios:

Edge-only – All tasks are processed at available edge nodes.

Cloud-only – All tasks are sent directly to the cloud.

Hybrid – Tasks are processed at the edge when possible, otherwise offloaded to the cloud.

Metrics recorded:

Average Latency (ms) per scenario.

Task Distribution across nodes.

The project uses SimPy for discrete-event simulation and Matplotlib for data visualization.

⚙️ Installation

git clone https://github.com/HariPrasannaKumar/Fog-and-Edge-Simulation.git cd Fog-and-Edge-Simulation

Master branch

pip install -r requirements.txt

▶️ Running the Simulation

Run all scenarios and generate graphs:

python main.py
