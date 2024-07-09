class Statter:
    def __init__(self):
        self.accumulator = 0.0
        self.instance_count = 0

    def add(self, quantity):
        self.accumulator += quantity
        self.instance_count += 1

    @property
    def mean(self):
        return self.accumulator / self.instance_count
