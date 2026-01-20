# Hybrid Perceptron-Based Branch Predictor

Computer Architecture | Python-Based Simulation

Accurate branch prediction is critical for maintaining high instruction throughput in
modern superscalar and deeply pipelined processors. Each branch misprediction introduces
control hazards, pipeline flushes, and wasted execution cycles, leading to increased CPI.

This project implements and evaluates multiple dynamic branch prediction techniques with
increasing sophistication to study their accuracy, performance impact, and hardware cost
trade-offs across different branch behaviors.

---

#### Software Components

- Language: Python
- Design Approach: Modular predictor framework
- Evaluation: Synthetic branch trace–based analysis

---

#### Predictors Implemented

- **2-bit Saturating Counter Predictor**  
  A simple table-based predictor that tracks short-term taken/not-taken behavior using
  2-bit finite state machines.

- **Perceptron-Based Branch Predictor**  
  A neural-inspired predictor that uses global branch history and weighted sums to learn
  long-range correlations in branch behavior.

- **Hybrid Branch Predictor**  
  Combines the 2-bit and perceptron predictors using a meta-selector that dynamically
  chooses the more accurate predictor for each branch.

---

#### Inputs

- Synthetic branch trace files in the format:  
  `<branch_address> <T/N>`
- Three workload types:
  - Loop-intensive trace
  - Complex correlated conditional trace
  - Highly irregular branch-heavy trace
- Each trace contains 5,000 dynamic branch outcomes

---

#### Operation

- Each predictor is implemented using a common interface for fair comparison.
- Branch outcomes are processed sequentially from trace files.
- Predictors generate taken/not-taken decisions and update internal state after resolution.
- A unified evaluation script runs all predictors on all traces.

---

#### Evaluation Metrics

- Prediction accuracy
- Mispredictions per thousand instructions (MPKI)
- Estimated CPI impact using a fixed 5-cycle misprediction penalty
- Approximate storage overhead for each predictor

---

#### Results Summary

- **Loop-Intensive Trace:**  
  Perceptron and hybrid predictors achieve near-perfect accuracy (~99.8%), while the
  2-bit predictor performs significantly worse due to limited learning capability.

- **Complex Correlated Trace:**  
  Perceptron predictor dominates with ~99.9% accuracy by learning long-range correlations.
  The hybrid predictor performs similarly, while the 2-bit predictor remains near 50%.

- **Highly Irregular (Branchy) Trace:**  
  All predictors converge near 50% accuracy, reflecting inherent unpredictability.
  The hybrid predictor shows slightly better robustness than the others.

- Low MPKI from perceptron and hybrid predictors translates directly to lower CPI.

---

#### Key Insights

- Perceptron predictors are highly effective for structured and correlated branch behavior.
- Simple 2-bit predictors are only effective for repetitive patterns such as loops.
- Hybrid prediction provides more stable performance across diverse workloads.
- Predictor complexity introduces trade-offs between accuracy, storage cost, and robustness.

---

#### Limitations

- Synthetic traces were used instead of real application traces.
- Predictors were simulated in Python rather than integrated into a cycle-accurate processor.
- Fixed misprediction penalty and simplified CPI estimation were used.

---

#### References

1. P. Seznec, *“A Comprehensive Look at Modern Branch Predictors,”* IEEE Micro, 2020.  
   https://ieeexplore.ieee.org/document/9099113

2. S. Sethumadhavan et al., *“Neural Branch Prediction: A 20-Year Retrospective,”* IEEE Computer, 2022.  
   https://ieeexplore.ieee.org/document/9833475

3. H. Wang et al., *“Tagenn: Combining TAGE with Neural Predictors for Hybrid Branch Prediction,”*  
   Proceedings of the International Symposium on Computer Architecture (ISCA), 2023.  
   https://ieeexplore.ieee.org/document/10158145

4. D. H. Schall and I. U. Schall, *“The Last-Level Branch Predictor,”*  
   Proceedings of the ACM/IEEE International Symposium on Computer Architecture (ISCA), June 2024.  
   https://ieeexplore.ieee.org/document/10546789

5. J. Yavarzadeh and S. Stefan, *“Half&Half: Demystifying Intel’s Directional Branch Predictors for Fast and Secure Execution,”*  
   IEEE Micro, October 2023.  
   https://ieeexplore.ieee.org/document/10288570

6. T. Nguyen et al., *“Reverse-Engineering Intel’s Latest Branch Predictors,”*  
   IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), 2023.  
   https://ieeexplore.ieee.org/document/10158174

