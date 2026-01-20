# Hybrid Perceptron-Based Branch Predictor

This project implements and evaluates dynamic branch prediction techniques to study their impact on instruction-level performance in pipelined processors.

## Overview
Accurate branch prediction is critical for maintaining high instruction throughput in modern processors. This project implements three predictors of increasing complexity:
- 2-bit saturating counter predictor
- Perceptron-based branch predictor
- Hybrid predictor combining both using a meta-selector

All predictors are evaluated under a unified Python framework to ensure fair and consistent comparison.

## Implemented Predictors
- **2-bit Predictor:** Simple finite-state predictor for short-term branch behavior.
- **Perceptron Predictor:** Neural-inspired predictor capturing long-range correlations.
- **Hybrid Predictor:** Selects the best predictor dynamically based on past accuracy.

## Experimental Setup
- Predictors implemented in **Python** with modular design.
- Evaluated on synthetic branch traces:
  - Loop-intensive workload
  - Complex conditional workload
  - Highly irregular branch-heavy workload
- Metrics evaluated:
  - Prediction accuracy
  - Mispredictions per thousand instructions (MPKI)
  - Estimated CPI impact
  - Storage overhead

## How to Run
```bash
python "final code to run/run_all.py"

