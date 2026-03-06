import matplotlib.pyplot as plt

# Load levels
load = [10]

# Latency percentiles
p50 = [6]
p95 = [25]
p99 = [60]

# Kernel metrics
tcp_retx = [6]
sched_delay = [11]

plt.figure()

plt.plot(load, p50, marker='o', label='p50 latency')
plt.plot(load, p95, marker='o', label='p95 latency')
plt.plot(load, p99, marker='o', label='p99 latency')

plt.xlabel("Connections")
plt.ylabel("Latency (ms)")
plt.title("Baseline Latency Measurement")
plt.legend()
plt.grid(True)

plt.savefig("latency_plot.png")
plt.show()
