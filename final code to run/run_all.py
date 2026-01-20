# experiments/run_all.py

import os, sys
sys.path.append(os.getcwd())

from utils.trace_loader import load_trace
from predictors.two_bit_predictor import TwoBitPredictor
from predictors.perceptron_predictor import PerceptronPredictor
from predictors.hybrid_predictor import HybridPredictor

# ----------------------------------------------------
# CONFIG (you can change these if your prof used others)
# ----------------------------------------------------
INSTRUCTIONS_PER_TRACE = 100_000   # assumed total dynamic instructions per 5000-branch trace
BASE_CPI = 1.0
MISPRED_PENALTY = 5.0              # cycles per misprediction

traces = {
    "loop": "traces/loop_5000.txt",
    "branchy": "traces/branchy_5000.txt",
    "complex": "traces/complex_5000.txt"
}

results = []   # predictor, trace, acc, correct, total, mpki, cpi

def compute_metrics(correct, total):
    misp = total - correct
    acc = correct / total if total > 0 else 0.0
    mpki = misp * 1000.0 / INSTRUCTIONS_PER_TRACE
    cpi  = BASE_CPI + MISPRED_PENALTY * mpki / 1000.0
    return acc, misp, mpki, cpi

# ----------------------------------------------------
# RUN EXPERIMENTS
# ----------------------------------------------------
for trace_name, trace_path in traces.items():
    print(f"\n=== Running on {trace_name} trace ===")
    trace = load_trace(trace_path)

    # 1. Two-bit
    two_bit = TwoBitPredictor(table_size=1024)
    acc, correct, total = two_bit.run_trace(trace)
    acc, misp, mpki, cpi = compute_metrics(correct, total)
    print(f"2-bit accuracy on {trace_name}: {acc:.4f}, MPKI={mpki:.2f}, CPI={cpi:.4f}")
    results.append(["2-bit", trace_name, acc, correct, total, misp, mpki, cpi])

    # 2. Perceptron
    percep = PerceptronPredictor(history_length=16, num_perceptrons=1024)
    acc, correct, total = percep.run_trace(trace)
    acc, misp, mpki, cpi = compute_metrics(correct, total)
    print(f"Perceptron accuracy on {trace_name}: {acc:.4f}, MPKI={mpki:.2f}, CPI={cpi:.4f}")
    results.append(["Perceptron", trace_name, acc, correct, total, misp, mpki, cpi])

    # 3. Hybrid
    hybrid = HybridPredictor(table_size=1024, history_length=16)
    acc, correct, total = hybrid.run_trace(trace)
    acc, misp, mpki, cpi = compute_metrics(correct, total)
    print(f"Hybrid accuracy on {trace_name}: {acc:.4f}, MPKI={mpki:.2f}, CPI={cpi:.4f}")
    results.append(["Hybrid", trace_name, acc, correct, total, misp, mpki, cpi])

# ----------------------------------------------------
# PRINT SUMMARY TABLE
# ----------------------------------------------------
print("\n\n==================== FINAL RESULTS ====================")
print("{:<12} {:<10} {:<9} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
    "Predictor", "Trace", "Accuracy", "Correct", "Total", "Misp", "MPKI", "CPI"))
print("------------------------------------------------------------------")

for p, t, a, c, tot, misp, mpki, cpi in results:
    print("{:<12} {:<10} {:<9.4f} {:<8} {:<8} {:<8} {:<8.2f} {:<8.4f}".format(
        p, t, a, c, tot, misp, mpki, cpi))

print("==================================================================")

