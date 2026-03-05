"""
Project ID: 9
File: 9_PartA_trace_sched.py

Trace CPU scheduling delays using eBPF
for analyzing tail latency in Kubernetes microservices.
"""

from bcc import BPF

program = """
TRACEPOINT_PROBE(sched, sched_switch) {
    bpf_trace_printk("CPU switch detected\\n");
    return 0;
}
"""

b = BPF(text=program)

print("Tracing CPU scheduling events... Press Ctrl-C to stop.")

b.trace_print()
