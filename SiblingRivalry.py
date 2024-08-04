import Models.InvaderPart,  Models.Decoy,   Models.Invader
import Models.Anvil,        Models.Furance, Models.Cannon
import Models.Resource,     Models.Weapon

class Game:
    def __init__(self):
        self.score = 0
        self.actions_taken = 0
        self.invaders_killed = 0

        self.gun_powder = 0         # divide by 5
        self.steel = 0              # divide by 5
        self.ore = 0                # divide by 250
        self.anvils = []            # 5
        self.furances = []          # 40
        self.weapons = []           # 40
        self.musketeerParts = []    # 4
        self.warriorParts = []      # 4
        self.musketeerDecoys = []   # 10 
        self.warriorDecoys = []     # 10
        self.musketeers = []        # 10
        self.warriors = []          # 10
        self.cannons = []           # 40
        self.gunpowderPile = []     # 4
        self.steelPile = []         # 4
        self.ironCrates = []        # 20

        # Currently not in use
        self.battemages = []        # 10
        self.battlemageDecoys = []  # 10
        self.flagGrunts = []        # 10
        self.spearGrunts = []       # 10
        self.swordGrunts = []       # 10
        
        self.action_mapping = {
            0: self.action_no_action,
            1: self.action_tap_worst_anvil,
            2: self.action_tap_best_anvil,
            3: self.action_merge_weapons,
            4: self.action_merge_invader_parts,
            5: self.action_collect_resource,
            6: self.action_merge_resources,
            7: self.action_attack_musketeer,
            8: self.action_attack_warrior,
            9: self.action_merge_anvil,
            10: self.action_merge_furnace,
            11: self.action_tap_decoy,
            12: self.action_discard,
            13: self.action_purchase_cannon,
            14: self.action_purchase_furnace,
            15: self.action_purchase_anvil,
        }

    # ACTION MASK
    def get_action_mask(self):
        mask = [True] * len(self.action_mapping)
        board_occupied = self.getBoardOccupied()
        # These policies are coupled to self.action_mapping:
        mask[0] = True
        mask[1] = bool(self.anvils) and board_occupied < 40
        mask[2] = bool(self.anvils) and board_occupied < 40
        mask[3] = self.mergeAble(self.weapons, 5)
        mask[4] = self.mergeAble(self.musketeerParts, 4) or self.mergeAble(self.warriorParts, 4)
        mask[5] = bool(self.ironCrates or self.gunpowderPile or self.steelPile)
        mask[6] = self.mergeAble(self.gunpowderPile, 3) or self.mergeAble(self.steelPile, 3)
        mask[7] = bool(self.musketeers)
        mask[8] = bool(self.warriors)
        mask[9] = self.mergeAble(self.anvils, 4)
        mask[10] = self.mergeAble(self.furances, 4)
        mask[11] = bool(self.musketeerDecoys or self.warriorDecoys)
        mask[12] = True
        mask[13] = self.gun_powder >= 20 and board_occupied < 40
        mask[14] = self.gun_powder >= 10 and self.steel >= 5 and board_occupied < 40
        mask[15] = self.steel >= 25  and board_occupied < 40
        return mask

    def mergeAble(self, object_list, limit):
        if len(object_list) < 2:
            return False
        for i in range(len(object_list) - 1):
            if object_list[i].level == object_list[i+1].level and object_list[i].level <= limit:
                return True
        return False
    
    def perform_action(self, action): # action is a number
        mask = self.get_action_mask()
        if action > len(mask) - 1 or action < 0:
            return -6969
        if not mask[action]:
            return -69
        
        action_function = self.action_mapping.get(action)
        if action_function:
            reward = action_function()
        else:
            print("Don't recognize action")
        stateOreProduced = self.getOreProduction()
        stateDamageProduced = self.getDamageProduction()
        self.updateOre(stateOreProduced)
        return reward + stateOreProduced + stateDamageProduced
    
    # DEFAULT GAME UPDATE
    # Returns reward value
    def getOreProduction(self):
        total_production = 0
        for f in self.furances:
            total_production += f.produceOre()
        return total_production
    
    def getDamageProduction(self):
        total_production = 0
        for c in self.cannons:
            total_production += c.getDamage()
        return total_production
    # Tinker with rewards

    # RETURN OBSERVATION
    def getObservation(self):
        obs = [
            self.gun_powder // 5,
            self.steel // 5,
            len(self.furances),
            int(self.getOreProduction() * 0.36),
            len(self.cannons),
            int(self.getDamageProduction() * 0.02),
            len(self.anvils),
            len(self.weapons),
            len(self.musketeerParts),
            len(self.warriorParts),
            len(self.musketeerDecoys),
            len(self.warriorDecoys),
            len(self.musketeers),
            len(self.warriors),
            len(self.gunpowderPile),
            len(self.steelPile),
            len(self.ironCrates)
        ]
        return obs
    
    def getBoardOccupied(self):
        return len(self.anvils) + len(self.furances) + len(self.weapons) + len(self.musketeerParts) + len(self.warriorParts) + len(self.musketeerDecoys) + len(self.warriorDecoys) + len(self.musketeers) + len(self.warriors) + len(self.cannons) + len(self.gunpowderPile) + len(self.steelPile) + len(self.ironCrates)

    def addToInventory(self, object):
        oc = object.__class__
        if oc == Models.Anvil.Anvil:
            self.anvils.append(object)
            self.anvils = sorted(self.anvils, key=lambda a : a.level)
        elif oc == Models.Furance.Furance:
            self.furances.append(object)
            self.furances = sorted(self.furances, key=lambda f : f.level)
        elif oc == Models.Weapon.Weapon:
            self.weapons.append(object)
            self.weapons = sorted(self.weapons, key=lambda f : f.level)
        elif oc == Models.InvaderPart.MusketeerPart:
            self.musketeerParts.append(object)
            self.musketeerParts = sorted(self.musketeerParts, key=lambda mp : mp.level)
        elif oc == Models.InvaderPart.WarriorPart:
            self.warriorParts.append(object)
            self.warriorParts = sorted(self.warriorParts, key=lambda wp : wp.level)
        elif oc == Models.Decoy.MusketeerDecoy:
            self.musketeerDecoys.append(object)
        elif oc == Models.Decoy.WarriorDecoy:
            self.warriorDecoys.append(object)
        elif oc == Models.Decoy.BattleMageDecoy:
            self.battlemageDecoys.append(object)
        elif oc == Models.Invader.FlagGrunt:
            self.flagGrunts.append(object)
        elif oc == Models.Invader.SpearGrunt:
            self.spearGrunts.append(object)
        elif oc == Models.Invader.SwordGrunt:
            self.swordGrunts.append(object)
        elif oc == Models.Invader.Musketeer:
            self.musketeers.append(object)
        elif oc == Models.Invader.Warrior:
            self.warriors.append(object)
        elif oc == Models.Invader.BattleMage:
            self.battemages.append(object)                
        elif oc == Models.Cannon.Cannon:
            self.cannons.append(object)
            self.cannons = sorted(self.cannons, key=lambda c : c.level)
        elif oc == Models.Resource.SteelPile:
            self.steelPile.append(object)
            self.steelPile = sorted(self.steelPile, key=lambda sp : sp.level)
        elif oc == Models.Resource.GunpowderPile:
            self.gunpowderPile.append(object)
            self.gunpowderPile = sorted(self.gunpowderPile, key=lambda gp : gp.level)
        elif oc == Models.Resource.IronCrate:
            self.ironCrates.append(object)
            self.ironCrates = sorted(self.ironCrates, key=lambda ic : ic.level)
        else:
            print("WARNING don't recognize object")
            return
        print("Added", oc.__name__)

    
    



    
    # ACTIONS
    # PRIORITY
    def action_no_action(self):
        return 0

    # PRIORITY
    def action_tap_worst_anvil(self):
        anvil = self.anvils[0]
        cost = anvil.getCost()
        anvil_product = anvil.tapProduction()
        self.addToInventory(anvil_product)
        self.updateOre(cost * -1)
        return 10

    # PRIORITY
    def action_tap_best_anvil(self):
        anvil = self.anvils[-1]
        cost = anvil.getCost()
        anvil_product = anvil.tapProduction()
        self.addToInventory(anvil_product)
        self.updateOre(cost * -1)
        return 10

    def action_attack_flag_grunt(self, damage):  # TODO Update to muskeeter function
        from Models.Resource import IronCrate
        if not self.flagGrunts:
            return -1
        flagGrunt = self.flagGrunts[0]
        flagGrunt.takeDamage(damage)
        if flagGrunt.getHealth() <= 0:
            self.flagGrunts.pop(0)
            self.addToInventory(IronCrate(1))
            self.updateKillCount()
            
            return 250 + damage + flagGrunt.getHealth() * 2
        return damage

    def action_attack_spear_grunt(self, damage):  # TODO
        from Models.Resource import GunpowderPile
        if not self.spearGrunts:
            return -1
        spear_grunt = self.spearGrunts[0]
        spear_grunt.takeDamage(damage)
        if spear_grunt.getHealth() <= 0:
            self.spearGrunts.pop(0)
            self.addToInventory(GunpowderPile(1))
            self.updateKillCount()
            
            return 500 + damage + spear_grunt.getHealth() * 2
        return damage

    def action_attack_sword_grunt(self, damage): # TODO
        from Models.Resource import SteelPile
        if not self.swordGrunts:
            return -1
        sword_grunt = self.swordGrunts[0]
        sword_grunt.takeDamage(damage)
        if sword_grunt.getHealth() <= 0:
            self.swordGrunts.pop(0)
            self.addToInventory(SteelPile(1))
            self.updateKillCount()
            return 1250 + damage + sword_grunt.getHealth() * 2
        return damage

    # PRIORITY
    def action_attack_musketeer(self): 
        from Models.Resource import GunpowderPile
        if not self.musketeers:
            return -1
        if not self.weapons or self.weapons[-1].level == 0:
            return -2
        weapon = self.weapons.pop()
        damage = weapon.getDamage()
        musketeer = self.musketeers[0]
        musketeer.takeDamage(damage)
        if musketeer.getHealth() <= 0:
            self.musketeers.pop(0)
            self.addToInventory(GunpowderPile(3))
            self.updateKillCount()
            return 15000 + damage + musketeer.getHealth() * 2
        return damage

    # PRIORITY
    def action_attack_warrior(self): 
        from Models.Resource import SteelPile
        if not self.warriors:
            return -1
        if not self.weapons or self.weapons[-1].level == 0:
            return -2
        weapon = self.weapons.pop()
        damage = weapon.getDamage()
        warrior = self.warriors[0]
        warrior.takeDamage(damage)
        if warrior.getHealth() <= 0:
            self.warriors.pop(0)
            self.addToInventory(SteelPile(3))
            self.updateKillCount()
            return 50000 + damage + warrior.getHealth() * 2
        return damage

    def action_attack_battle_mage(self, damage):
        pass

    # PRIORIY
    # Manages steel and gunpowder
    def action_merge_resources(self):
        from Models.Resource import GunpowderPile
        if len(self.gunpowderPile) < 2:
            return -1
        for i in range(len(self.gunpowderPile) - 1):
            f, s = self.gunpowderPile[i], self.gunpowderPile[i+1]
            new_gunpowderPile = GunpowderPile.mergeResource(f,s)
            if len(new_gunpowderPile) == 1:
                self.gunpowderPile.pop(i)
                
                self.gunpowderPile.pop(i)
                
                self.gunpowderPile.insert(i, new_gunpowderPile[0])
                return new_gunpowderPile[0].getResourceValue()
        return -1

    # PRIORITY
    def action_merge_invader_parts(self): # TODO
        from Models.InvaderPart import MusketeerPart, WarriorPart
        if len(self.musketeerParts) > 1:
            for i in range(len(self.musketeerParts) - 1):
                f, s = self.musketeerParts[i], self.musketeerParts[i+1]
                new_musketeerParts = MusketeerPart.mergePart(f,s)
                if len(new_musketeerParts) == 1:
                    self.musketeerParts.pop(i)
                    
                    self.musketeerParts.pop(i)
                    
                    self.addToInventory(new_musketeerParts[0])
                    return 69
        if len(self.warriorParts) > 1:
            for i in range(len(self.warriorParts) - 1):
                f, s = self.warriorParts[i], self.warriorParts[i+1]
                new_warriorParts = WarriorPart.mergePart(f,s)
                if len(new_warriorParts) == 1:
                    self.warriorParts.pop(i)
                    
                    self.warriorParts.pop(i)
                    
                    self.addToInventory(new_warriorParts[0])
                    return 6969    
        return -1

    # PRIORITY
    def action_merge_furnace(self):
        from Models.Furance import Furance
        if len(self.furances) < 2:
            return -1
        for i in range(len(self.furances) - 1):
            f, s = self.furances[i], self.furances[i+1]
            new_furances = Furance.mergeFurance(f,s)
            if len(new_furances) == 1:
                self.furances.pop(i)
                
                self.furances.pop(i)
                
                self.addToInventory(new_furances[0])

                return new_furances[0].level
        return -1

    # PRIORITY
    def action_merge_weapons(self):
        from Models.Weapon import Weapon
        if len(self.weapons) < 2:
            return -1
        for i in range(len(self.weapons) - 1):
            f, s = self.weapons[i], self.weapons[i+1]
            new_weapons = Weapon.mergeWeapon(f,s)
            if len(new_weapons) == 1:
                self.weapons.pop(i)
                
                self.weapons.pop(i)
                
                self.addToInventory(new_weapons[0])
                return new_weapons[0].getDamage()
        return -1

    # PRIORITY
    def action_merge_anvil(self):
        from Models.Anvil import Anvil
        if len(self.anvils) < 2:
            return -1
        for i in range(len(self.anvils) - 1):
            f, s = self.anvils[i], self.anvils[i+1]
            new_anvils = Anvil.mergeAnvil(f,s)
            if len(new_anvils) == 1:
                self.anvils.pop(i)
                
                self.anvils.pop(i)
                
                self.addToInventory(new_anvils[0])
                return new_anvils[0].level
        return -2
    
    # PRIORITY
    def action_tap_decoy(self):
        if len(self.warriorDecoys) > 0:
            warrior_decoy = self.warriorDecoys.pop(0)
            warrior = warrior_decoy.tapToSummon()
            self.addToInventory(warrior)
            return 25000
        if len(self.musketeerDecoys) > 0:
            muskeeter_decoy = self.musketeerDecoys.pop(0)
            muskeeter = muskeeter_decoy.tapToSummon()
            self.addToInventory(muskeeter)
            return 10000
        return -1

    # PRIORITY
    def action_discard(self):
        if self.weapons:
            weapon = self.weapons.pop(0)
            return weapon.getDamage() * -1
        elif self.musketeerParts:
            mp = self.musketeerParts.pop(0)
            return  mp.level * -1000
        elif self.warriorParts:
            wp = self.warriorParts.pop(0)
            return  wp.level * -2500
        elif self.cannons:
            c = self.cannons.pop(0)
            return  c.level * -1000
        elif self.furances:
            f = self.furances.pop(0)
            return  f.level * -10000
        elif self.anvils:
            a = self.anvils.pop(0)
            return  a.level * -100000
        else:
            return -1000000

    def action_summon_banner(self):
        pass

    def action_tap_banner(self):
        pass

    # PRIORITY
    def action_collect_resource(self): # could be split into three
        if len(self.ironCrates) > 0:
            ic = self.ironCrates.pop()
            self.updateOre(ic.getResourceValue())
            return ic.getResourceValue()
        if len(self.gunpowderPile) > 0:
            gp = self.gunpowderPile.pop()
            self.updateGunpowder(gp.getResourceValue())
            return gp.getResourceValue()
        if len(self.steelPile) > 0:
            s = self.steelPile.pop()
            self.updateSteel(s.getResourceValue())
            return s.getResourceValue()
        return -1


    # PRIORITY: 
    def action_purchase_cannon(self): 
        from Models.Cannon import Cannon
        if self.gun_powder < 20:
            return -1
        self.updateGunpowder(-20)
        self.addToInventory(Cannon(1))
        remaining_damage = 100
        cost_of_gp = -100
        return remaining_damage + cost_of_gp

    def action_purchase_furnace(self): 
        from Models.Furance import Furance
        if self.gun_powder < 10 or self.steel < 5:
            return -1
        self.updateGunpowder(-10)
        self.updateSteel(-5)
        self.addToInventory(Furance(1))
        remaining_ore = 100
        cost_of_gp = -50
        cost_of_s = -50
        return remaining_ore + cost_of_gp + cost_of_s

    def action_purchase_anvil(self):
        from Models.Anvil import Anvil
        if self.steel < 25:
            return -1
        self.updateSteel(-25)
        self.addToInventory(Anvil(1))
        remaining_value = 100
        cost_of_s = -100
        return remaining_value + cost_of_s 

    def action_purchase_from_trade(self): # should be split
        pass

    def action_purchase_upgrade(self): # should be split
        pass







    # UTILITIES
    def updateScore(self, score):
        self.score = self.score + score

    def updateSteel(self, steel):
        self.steel = self.steel + steel
    
    def updateGunpowder(self, gun_powder):
        self.gun_powder = self.gun_powder + gun_powder

    def updateOre(self, ore):
        self.ore = self.ore + ore
    
    def updateKillCount(self):
        self.invaders_killed += 1

    def getResources(self):
        return self.ironCrates + self.gunpowderPile + self.steelPile
    
    def getInvaders(self):
        invaders = self.flagGrunts + self.spearGrunts + self.swordGrunts + self.musketeers + self.warriors
        invaders = sorted(invaders, key=lambda i : i.health)
        return invaders
    
    def getStructures(self):
        return self.anvils + self.furances + self.cannons
    
    def getMisc(self):
        return self.musketeerParts + self.musketeerDecoys + self.warriorParts + self.warriorDecoys

    def render(self):
        print("---------------------------------------------------------------------------------")
        print(f"Score\t\t\t{self.score}\tStructures\t", self.getStructures())
        print(f"Ore\t\t\t{self.ore}\tResources\t", self.getResources())
        print(f"Gunpowder\t\t{self.gun_powder}\tInvaders\t", self.getInvaders())
        print(f"Steel\t\t\t{self.steel}\tParts & Decoys\t", self.getMisc())
        print(f"Invaders Killed\t\t{self.invaders_killed}\tWeapons\t\t", self.weapons)
        print(f"Action Taken\t\t{self.actions_taken}\tBoard Occupied\t", self.getBoardOccupied())
        print("---------------------------------------------------------------------------------")

    def reset(self):
        self.score = 0
        self.gun_powder = 0
        self.steel = 0        
        self.ore = 50000
        self.actions_taken = 0
        self.anvils = []
        self.furances = []
        self.weapons = []
        self.musketeerParts = []
        self.warriorParts = []
        self.musketeerDecoys = []
        self.warriorDecoys = []
        self.battlemageDecoys = []
        self.flagGrunts = []
        self.spearGrunts = []
        self.swordGrunts = []
        self.musketeers = []
        self.warriors = []
        self.battemages = []
        self.cannons = []
        self.gunpowderPile = []
        self.steelPile = []
        self.ironCrates = []

    def getOre(self) -> int:
        return self.ore
    
# TEST
    
if __name__ == "__main__":
    g1 = Game()
    a1 = Models.Anvil.Anvil(1)
    a2 = Models.Anvil.Anvil(2)
    a3 = Models.Anvil.Anvil(3)
    a4 = Models.Anvil.Anvil(4)
    f1 = Models.Furance.Furance(1)
    f2 = Models.Furance.Furance(1)
    f3 = Models.Furance.Furance(2)
    f4 = Models.Furance.Furance(2)
    f5 = Models.Furance.Furance(3)
    f6 = Models.Furance.Furance(3)
    c1 = Models.Cannon.Cannon(1)
    c2 = Models.Cannon.Cannon(1)
    c3 = Models.Cannon.Cannon(1)
    c4 = Models.Cannon.Cannon(1)
    md1 = Models.Decoy.MusketeerDecoy()
    wd1 = Models.Decoy.WarriorDecoy()
    bm1 = Models.Decoy.BattleMageDecoy()
    i1 = Models.Invader.FlagGrunt()
    i2 = Models.Invader.SpearGrunt()
    i3 = Models.Invader.SwordGrunt()
    i4 = Models.Invader.Musketeer()
    i5 = Models.Invader.Warrior()
    i6 = Models.Invader.BattleMage()
    mp1 = Models.InvaderPart.MusketeerPart(4)
    mp2 = Models.InvaderPart.MusketeerPart(4)
    wp1 = Models.InvaderPart.WarriorPart(4)
    wp2 = Models.InvaderPart.WarriorPart(4)
    r1 = Models.Resource.GunpowderPile(1)
    r2 = Models.Resource.GunpowderPile(1)
    r3 = Models.Resource.GunpowderPile(1)
    r4 = Models.Resource.GunpowderPile(1)
    
    # r2 = Models.Resource.SteelPile(1)
    # r3 = Models.Resource.IronCrate(1)
    w1 = Models.Weapon.Weapon(6)
    w2 = Models.Weapon.Weapon(6)
    w3 = Models.Weapon.Weapon(5)
    w4 = Models.Weapon.Weapon(5)
    g1.updateOre(50000)
    g1.updateGunpowder(25)
    g1.addToInventory(a1)
    g1.addToInventory(f1)
    g1.addToInventory(f2)
    g1.addToInventory(f3)
    g1.addToInventory(f4)
    g1.addToInventory(f5)
    g1.addToInventory(f6)
    g1.addToInventory(w1)
    g1.addToInventory(w2)
    g1.addToInventory(i4)

    while True:
        g1.render()
        print(g1.get_action_mask())
        print(g1.getObservation())
        user_input = input("\nPerform Action: ").strip().lower()
        try:
            user_input = int(user_input)
            if user_input == -1:
                break
            print("Reward received:", g1.perform_action(user_input),"\n")
        except:
            print("Action not recognized")
        

        

# class AlchemyTable:

