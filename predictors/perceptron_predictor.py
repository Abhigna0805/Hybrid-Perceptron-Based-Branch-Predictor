# predictors/perceptron_predictor.py

import math

class PerceptronPredictor:
    """
    Perceptron branch predictor.
    Uses:
    - A global history register (GHR)
    - A table of perceptrons
    - Dot product prediction
    - Threshold-based training rule
    """

    def __init__(self, history_length=16, num_perceptrons=1024):
        self.history_length = history_length
        self.num_perceptrons = num_perceptrons

        # Weight table: each perceptron has (history_length + 1) weights including bias
        self.weights = [[0] * (history_length + 1) for _ in range(num_perceptrons)]

        # Global history register storing +1 / -1
        self.ghr = [1] * history_length

        # Training threshold as suggested in the paper
        self.threshold = int(1.93 * history_length + 14)

    def _index(self, addr):
        return addr % self.num_perceptrons

    def predict(self, addr):
        idx = self._index(addr)
        w = self.weights[idx]

        # Dot product: bias + sum(w_i * history_i)
        output = w[0]
        for i in range(self.history_length):
            output += w[i + 1] * self.ghr[i]

        prediction = (output >= 0)
        return prediction, output

    def update(self, addr, actual_taken, output):
        idx = self._index(addr)
        w = self.weights[idx]

        actual = 1 if actual_taken else -1

        # Update if prediction is wrong or not confident
        if (actual_taken and output < 0) or (not actual_taken and output >= 0) or abs(output) < self.threshold:

            # Update bias
            w[0] += actual

            # Update weights
            for i in range(self.history_length):
                w[i + 1] += actual * self.ghr[i]

        # Shift GHR
        self.ghr = [actual] + self.ghr[:-1]

    def run_trace(self, trace):
        correct = 0
        total = 0

        for addr, actual in trace:
            pred, output = self.predict(addr)
            if pred == actual:
                correct += 1
            self.update(addr, actual, output)
            total += 1

        accuracy = correct / total if total > 0 else 0.0
        return accuracy, correct, total
