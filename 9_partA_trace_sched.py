"""
Project ID: 9
File: 9_partA_trace_sched.py

Trace CPU scheduling events using eBPF
and report counts every 10 seconds.
"""

from bcc import BPF
import time
import ctypes as ct

program = """
BPF_HASH(counter, u64, u64);

TRACEPOINT_PROBE(sched, sched_switch) {
    u64 key = 0;
    u64 init_val = 1;
    u64 *val = counter.lookup(&key);

    if (val) {
        (*val)++;
    } else {
        counter.update(&key, &init_val);
    }
    return 0;
}
"""

b = BPF(text=program)

print("Tracing CPU scheduling events... Press Ctrl-C to stop.", flush=True)

key = ct.c_ulonglong(0)
table = b.get_table("counter")

try:
    while True:
        time.sleep(10)

        if key in table:
            count = table[key].value
            print(f"[10s summary] CPU context switches = {count}", flush=True)
            table.clear()
        else:
            print("[10s summary] CPU context switches = 0", flush=True)

except KeyboardInterrupt:
    print("\nStopping trace...", flush=True)
