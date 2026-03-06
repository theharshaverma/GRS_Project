"""
Project ID: 9
File: 9_partA_trace_tcp.py

Trace TCP retransmissions using eBPF and report counts every 10 seconds
"""

from bcc import BPF
import time
import ctypes as ct

program = """
BPF_HASH(counter, u64, u64);

TRACEPOINT_PROBE(tcp, tcp_retransmit_skb) {
    u64 key = 0;
    u64 init_val = 1;
    u64 *val;

    val = counter.lookup(&key);
    if (val) {
        (*val)++;
    } else {
        counter.update(&key, &init_val);
    }
    return 0;
}
"""

b = BPF(text=program)

print("Tracing TCP retransmissions... Press Ctrl-C to stop.", flush=True)

key = ct.c_ulonglong(0)

try:
    while True:
        time.sleep(10)
        table = b.get_table("counter")

        if key in table:
            count = table[key].value
            print(f"[10s summary] TCP retransmissions = {count}", flush=True)
            table.clear()
        else:
            print("[10s summary] TCP retransmissions = 0", flush=True)

except KeyboardInterrupt:
    print("\nStopping trace...", flush=True)
