import matplotlib.pyplot as plt

load = [10, 100]

p50 = [6, 12]
p95 = [25, 40]
p99 = [60, 80]

plt.plot(load, p50, marker='o', label='p50')
plt.plot(load, p95, marker='o', label='p95')
plt.plot(load, p99, marker='o', label='p99')

plt.xlabel("Connections")
plt.ylabel("Latency (ms)")
plt.title("Latency vs Load")
plt.legend()
plt.grid(True)

plt.savefig("latency_plot.png")
plt.show()
