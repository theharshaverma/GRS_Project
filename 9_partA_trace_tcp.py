"""
Project ID: 9
File: 9_partA_trace_tcp.py

Trace TCP retransmissions using eBPF
"""

from bcc import BPF

program = """
TRACEPOINT_PROBE(tcp, tcp_retransmit_skb) {
    bpf_trace_printk("TCP retransmission detected\\n");
    return 0;
}
"""

b = BPF(text=program)

print("Tracing TCP retransmissions... Press Ctrl-C to stop.")

b.trace_print()
