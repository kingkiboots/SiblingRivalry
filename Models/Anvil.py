import random
from Weapon import Weapon
from InvaderPart import MusketeerPart, WarriorPart

class Anvil:
    anvil_cost_map = {1:250, 2:500, 3:750, 4:1000, 5:1500}
    # P Index is as follows: W0, MP1, WP1, MP2, WP2
    anvil_tap_map = {1:[0.95, 1.0, 0, 0, 0],
                     2:[0.85, 0.95, 1.0, 0, 0],
                     3:[0.65, 0.80, 0.9, 1.0, 0],
                     4:[0.30, 0.60, 0.8, 1.0, 0],
                     5:[0.10, 0.40, 0.70, 0.90, 1.0]}
    
    def __init__(self, level):
        self.level = level
    
    def getLevel(self):
        return self.level

    def tapProduction(self):
        anvil_p = Anvil.anvil_tap_map[self.level]

        p = random.random()
        summon_index = 0

        for i in range(len(anvil_p)):
            if p <= anvil_p[i]:
                summon_index = i
                break
        
        if summon_index == 0:
            return Weapon(0)
        elif summon_index == 1:
            return MusketeerPart(1)
        elif summon_index == 2:
            return WarriorPart(1)
        elif summon_index == 3:
            return MusketeerPart(2)
        elif summon_index == 4:
            return WarriorPart(2)
    
    @classmethod
    def mergeAnvil(cls, w1, w2):
        if w1.getLevel() != w2.getLevel():
            return [w1,w2]
        
        if w1.getLevel() < 4:
            return cls(w1.getLevel() + 1)
        else:
            return cls(w1.getLevel())

#Test

# a1 = Anvil(1)
# a2 = Anvil(2)
# a3 = Anvil(3)
# a4 = Anvil(4)
# a5 = Anvil(5)

# s1 = a1.tapProduction()
# print(s1.description, "\n")
# s2 = a2.tapProduction()
# print(s2.description, "\n")
# s3 = a3.tapProduction()
# print(s3.description, "\n")
# s4 = a4.tapProduction()
# print(s4.description, "\n")
# s5 = a5.tapProduction()
# print(s5.description, "\n")




