# utils/trace_loader.py

def load_trace(filepath):
    """
    Reads a branch trace file.
    Each line: <hex_address> <T_or_N>
    Returns a list of (address:int, outcome:bool) where True = taken.
    """
    trace = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            addr_str, outcome_str = line.split()
            addr = int(addr_str, 16)
            taken = outcome_str.upper() == "T"
            trace.append((addr, taken))
    return trace


if __name__ == "__main__":
    # quick sanity check
    from pathlib import Path

    sample = Path(__file__).resolve().parents[1] / "traces" / "sample_trace.txt"
    if sample.exists():
        data = load_trace(sample)
        print(f"Loaded {len(data)} branches")
        print(data[:5])
    else:
        print("No sample_trace.txt found, but loader is ready.")

