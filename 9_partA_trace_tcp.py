"""
Project ID: 9
File: 9_partA_trace_tcp.py

Trace TCP retransmissions using eBPF and report counts every 10 seconds
"""

from bcc import BPF
import time

program = """
BPF_HASH(counter, u64, u64);

TRACEPOINT_PROBE(tcp, tcp_retransmit_skb) {
    u64 key = 0;
    u64 *val = counter.lookup(&key);

    if (val) {
        (*val)++;
    } else {
        u64 init = 1;
        counter.update(&key, &init);
    }

    return 0;
}
"""

b = BPF(text=program)

print("Tracing TCP retransmissions... Press Ctrl-C to stop.")

try:
    while True:
        time.sleep(10)

        key = 0
        count = b["counter"].get(key)

        if count:
            print(f"[10s summary] TCP retransmissions = {count.value}")
            b["counter"].clear()
        else:
            print("[10s summary] TCP retransmissions = 0")

except KeyboardInterrupt:
    print("\nStopping trace...")
