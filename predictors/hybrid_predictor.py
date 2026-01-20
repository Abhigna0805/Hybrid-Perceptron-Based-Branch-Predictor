# predictors/hybrid_predictor.py

from predictors.two_bit_predictor import TwoBitPredictor
from predictors.perceptron_predictor import PerceptronPredictor

class HybridPredictor:
    """
    Hybrid predictor combining:
    - 2-bit saturating counter predictor
    - Perceptron predictor
    Using a meta predictor (2-bit selector)
    """

    def __init__(self, table_size=1024, history_length=16):
        self.table_size = table_size

        # Components
        self.two_bit = TwoBitPredictor(table_size=table_size)
        self.perceptron = PerceptronPredictor(history_length=history_length,
                                              num_perceptrons=table_size)

        # Selector table: 2-bit counters, initialized to weakly choose 2-bit (01)
        self.selector = [1] * table_size

    def _index(self, addr):
        return addr % self.table_size

    def predict(self, addr):
        idx = self._index(addr)

        # Predictions from both predictors
        two_bit_pred = self.two_bit.predict(addr)
        percep_pred, percep_output = self.perceptron.predict(addr)

        # Selector decides which prediction to return
        use_percep = self.selector[idx] >= 2
        final_prediction = percep_pred if use_percep else two_bit_pred

        return final_prediction, two_bit_pred, (percep_pred, percep_output)

    def update(self, addr, actual_taken, two_bit_pred, percep_pred, percep_output):
        idx = self._index(addr)

        # Update child predictors
        self.two_bit.update(addr, actual_taken)
        self.perceptron.update(addr, actual_taken, percep_output)

        # Update selector based on correctness
        two_bit_correct = (two_bit_pred == actual_taken)
        percep_correct = (percep_pred == actual_taken)

        if percep_correct and not two_bit_correct:
            self.selector[idx] = min(self.selector[idx] + 1, 3)
        elif two_bit_correct and not percep_correct:
            self.selector[idx] = max(self.selector[idx] - 1, 0)
        # If both correct or both wrong → do nothing

    def run_trace(self, trace):
        correct = 0
        total = 0

        for addr, actual in trace:
            final_pred, two_bit_pred, (percep_pred, percep_output) = self.predict(addr)

            if final_pred == actual:
                correct += 1

            self.update(addr, actual, two_bit_pred, percep_pred, percep_output)
            total += 1

        accuracy = correct / total if total > 0 else 0.0
        return accuracy, correct, total
