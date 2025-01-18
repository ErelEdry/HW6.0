import random
class Dice:
    def roll(self):
        self.rolled_num= random.randint(1,6)
        return self.rolled_num