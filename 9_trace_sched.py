"""
Project ID: 9
File: 9_partA_trace_sched.py

Measure wakeup-to-run scheduling delay using eBPF
and report summary statistics every 10 seconds.
"""

from bcc import BPF
import ctypes as ct
import time

program = r"""
#include <linux/sched.h>

BPF_HASH(wakeup_ts, u32, u64);

struct stats_t {
    u64 count;
    u64 total_ns;
    u64 max_ns;
};

BPF_HASH(stats, u32, struct stats_t);

TRACEPOINT_PROBE(sched, sched_wakeup) {
    u32 pid = args->pid;
    u64 ts = bpf_ktime_get_ns();
    wakeup_ts.update(&pid, &ts);
    return 0;
}

TRACEPOINT_PROBE(sched, sched_wakeup_new) {
    u32 pid = args->pid;
    u64 ts = bpf_ktime_get_ns();
    wakeup_ts.update(&pid, &ts);
    return 0;
}

TRACEPOINT_PROBE(sched, sched_switch) {
    u32 next_pid = args->next_pid;
    u64 *tsp, delta;
    u32 key = 0;
    struct stats_t zero = {};
    struct stats_t *s;
    u64 now = bpf_ktime_get_ns();

    tsp = wakeup_ts.lookup(&next_pid);
    if (!tsp) {
        return 0;
    }

    delta = now - *tsp;
    wakeup_ts.delete(&next_pid);

    s = stats.lookup(&key);
    if (!s) {
        stats.update(&key, &zero);
        s = stats.lookup(&key);
        if (!s) {
            return 0;
        }
    }

    s->count += 1;
    s->total_ns += delta;
    if (delta > s->max_ns) {
        s->max_ns = delta;
    }

    return 0;
}
"""

class Stats(ct.Structure):
    _fields_ = [
        ("count", ct.c_ulonglong),
        ("total_ns", ct.c_ulonglong),
        ("max_ns", ct.c_ulonglong),
    ]

b = BPF(text=program)

print("Tracing wakeup-to-run scheduling delay... Press Ctrl-C to stop.", flush=True)

key = ct.c_uint(0)
table = b.get_table("stats", ct.c_uint, Stats)

try:
    while True:
        time.sleep(10)

        if key in table:
            s = table[key]
            count = s.count
            total_ns = s.total_ns
            max_ns = s.max_ns

            avg_us = (total_ns / count) / 1000.0 if count > 0 else 0.0
            max_us = max_ns / 1000.0

            print(
                f"[10s summary] wakeup->run events = {count}, "
                f"avg delay = {avg_us:.2f} us, "
                f"max delay = {max_us:.2f} us",
                flush=True,
            )

            table.clear()
        else:
            print(
                "[10s summary] wakeup->run events = 0, avg delay = 0.00 us, max delay = 0.00 us",
                flush=True,
            )

except KeyboardInterrupt:
    print("\nStopping trace...", flush=True)
