### Hybrid Perceptron-Based Branch Predictor

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

1. D. A. Jiménez and C. Lin, *“Neural Methods for Dynamic Branch Prediction,”* ACM Transactions on Computer Systems, 2002.  
   https://www.cs.utexas.edu/~lin/papers/tocs02.pdf :contentReference[oaicite:0]{index=0}

2. T. Ball and J. Larus, *“Branch Prediction for Free,”* Proceedings of the SIGPLAN ’93 Conference on Programming Language Design and Implementation, 1993.  
   https://scholar.google.com/scholar?q=Branch+Prediction+for+Free+Ball+Larus

3. T. Y. Yeh and Y. N. Patt, *“Two-Level Adaptive Training Branch Prediction,”* Proceedings of the International Symposium on Computer Architecture (ISCA), 1993.  
   https://scholar.google.com/scholar?q=Two-Level+Adaptive+Training+Branch+Prediction+Yeh+Patt

4. C.-C. Lee, C. C. Chen, and T. N. Mudge, *“The Bi-Mode Branch Predictor,”* Proceedings of the 30th International Symposium on Computer Architecture, 1997.  
   https://scholar.google.com/scholar?q=Bi-Mode+Branch+Predictor+Lee+Chen+Mudge

5. Zangeneh et al., *“BranchNet: A Convolutional Neural Network to Predict Hard Branches,”* Microarchitecture paper (online PDF).  
   https://hps.ece.utexas.edu/pub/BranchNet_Micro2020.pdf :contentReference[oaicite:1]{index=1}


