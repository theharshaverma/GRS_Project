import matplotlib.pyplot as plt

# Experiment loads
load = [10, 100, 300]

# Latency values (ms)
p50 = [6, 12, 17]
p95 = [25, 40, 90]
p99 = [60, 80, 170]

plt.figure()

plt.plot(load, p50, marker='o', label='P50')
plt.plot(load, p95, marker='o', label='P95')
plt.plot(load, p99, marker='o', label='P99')

plt.xlabel("Connections")
plt.ylabel("Latency (ms)")
plt.title("Latency vs Load in Kubernetes Microservice")

plt.legend()
plt.grid(True)

plt.savefig("latency_plot.png")
plt.show()
