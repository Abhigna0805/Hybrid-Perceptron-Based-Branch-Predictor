# predictors/two_bit_predictor.py

class TwoBitPredictor:
    """
    Simple 2-bit saturating counter branch predictor.
    """

    def __init__(self, table_size=1024):
        self.table_size = table_size
        self.counter_table = [1] * table_size   # init with weakly NOT taken (01)

    def _index(self, addr):
        return addr % self.table_size

    def predict(self, addr):
        idx = self._index(addr)
        counter = self.counter_table[idx]
        return counter >= 2    # 2 or 3 means predict TAKEN

    def update(self, addr, actual_taken):
        idx = self._index(addr)
        counter = self.counter_table[idx]

        if actual_taken:
            counter = min(counter + 1, 3)
        else:
            counter = max(counter - 1, 0)

        self.counter_table[idx] = counter

    def run_trace(self, trace):
        """
        Runs the predictor on a trace loaded from trace_loader.
        trace = list of (address:int, taken:bool)
        Returns accuracy.
        """
        correct = 0
        total = 0

        for addr, actual in trace:
            prediction = self.predict(addr)
            if prediction == actual:
                correct += 1
            self.update(addr, actual)
            total += 1

        accuracy = correct / total if total > 0 else 0
        return accuracy, correct, total
