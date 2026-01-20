# generate_traces.py
# Generates 3 large branch trace files (5000 lines each)

import random
from pathlib import Path

TRACE_DIR = Path("traces")
TRACE_DIR.mkdir(exist_ok=True)

def generate_loop_trace(filename, n=5000):
    """
    Mostly taken loop pattern: T T T T N repeating.
    Great for 2-bit predictor.
    """
    with open(TRACE_DIR / filename, "w") as f:
        pattern = ["T", "T", "T", "T", "N"]
        addr = "0x1000"
        for i in range(n):
            f.write(f"{addr} {pattern[i % 5]}\n")


def generate_branchy_trace(filename, n=5000):
    """
    Mixed predictable/unpredictable patterns.
    Good for comparing 2-bit vs perceptron.
    """
    with open(TRACE_DIR / filename, "w") as f:
        addrs = ["0x3450", "0x7800", "0xAB10", "0xF200", "0x9000"]
        for i in range(n):
            addr = random.choice(addrs)
            # 50–50 random behavior
            outcome = "T" if random.random() > 0.5 else "N"
            f.write(f"{addr} {outcome}\n")


def generate_complex_trace(filename, n=5000):
    """
    Long-correlation pattern: T N T T T N repeating,
    plus multiple correlated addresses.
    Great for perceptron & hybrid predictors.
    """
    with open(TRACE_DIR / filename, "w") as f:
        pattern = ["T", "N", "T", "T", "T", "N"]
        addrs = ["0x8000", "0xA123", "0xB555"]
        for i in range(n):
            addr = addrs[i % 3]
            outcome = pattern[i % 6]
            f.write(f"{addr} {outcome}\n")


if __name__ == "__main__":
    print("Generating 5000-line trace files...")

    generate_loop_trace("loop_5000.txt")
    generate_branchy_trace("branchy_5000.txt")
    generate_complex_trace("complex_5000.txt")

    print("Done!")
    print("Created:")
    print(" - traces/loop_5000.txt")
    print(" - traces/branchy_5000.txt")
    print(" - traces/complex_5000.txt")
