import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Plot power consumption data.')
parser.add_argument("path", type=str, help='Path to the power data directory')
parser.add_argument("--output", "-o", type=str, default=None, help='Output file for the plot')
args = parser.parse_args()

if args.output is None:
    output_file = 'power_consumption.png'

def read_power_file(filepath):
    """Read power data from a file and return power values and timestamps."""
    power = []
    timestamps = []
    
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                power.append(float(parts[0]))  # Power in W
                timestamps.append(float(parts[2]) / 1e6)  # Convert microseconds to seconds
    
    return np.array(timestamps), np.array(power)

# Define the data directory
data_dir = Path(args.path)

# Read CPU power data
cpu_data = {}
for i in range(4):
    filepath = data_dir / f'cpu{i}_power.txt'
    timestamps, power = read_power_file(filepath)
    cpu_data[f'CPU{i}'] = (timestamps, power)

# Read GPU power data
gpu_data = {}
for i in range(4):
    filepath = data_dir / f'gpu{i}_power.txt'
    timestamps, power = read_power_file(filepath)
    gpu_data[f'GPU{i}'] = (timestamps, power)

# Read node power data
node_timestamps, node_power = read_power_file(data_dir / 'node_power.txt')

# Normalize timestamps to start from 0
def normalize_timestamps(timestamps):
    return timestamps - timestamps[0]

# Create figure with subplots
fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Top left: CPU power
ax1 = fig.add_subplot(gs[0, 0])
for cpu_name, (timestamps, power) in cpu_data.items():
    norm_timestamps = normalize_timestamps(timestamps)
    ax1.plot(norm_timestamps, power, label=cpu_name, linewidth=1.5, alpha=0.8, marker='o', markersize=1.5)

ax1.set_xlabel('Time (s)', fontsize=11)
ax1.set_ylabel('Power (W)', fontsize=11)
ax1.set_title('CPU Power Consumption', fontsize=13, fontweight='bold')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)

# Top right: GPU power
ax2 = fig.add_subplot(gs[0, 1])
for gpu_name, (timestamps, power) in gpu_data.items():
    norm_timestamps = normalize_timestamps(timestamps)
    ax2.plot(norm_timestamps, power, label=gpu_name, linewidth=1.5, alpha=0.8, marker='o', markersize=1.5)

ax2.set_xlabel('Time (s)', fontsize=11)
ax2.set_ylabel('Power (W)', fontsize=11)
ax2.set_title('GPU Power Consumption', fontsize=13, fontweight='bold')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)

# Bottom: Node power (spanning both columns)
ax3 = fig.add_subplot(gs[1, :])
norm_node_timestamps = normalize_timestamps(node_timestamps)
ax3.plot(norm_node_timestamps, node_power, label='Node Power', 
         linewidth=2, alpha=0.8, color='darkgreen', marker='x', markersize=2)

ax3.set_xlabel('Time (s)', fontsize=11)
ax3.set_ylabel('Power (W)', fontsize=11)
ax3.set_title('Total Node Power Consumption', fontsize=13, fontweight='bold')
ax3.legend(loc='best')
ax3.grid(True, alpha=0.3)

# Add overall title
fig.suptitle('Power Consumption Analysis', fontsize=15, fontweight='bold', y=0.995)

# Save the figure
plt.savefig(args.output, dpi=600, bbox_inches='tight')
