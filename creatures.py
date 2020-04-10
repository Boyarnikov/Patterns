class Unit:
    def __init__(self, hp, grp, spd, pwr):
        self.health = hp
        self.groupid = grp
        self.speed = spd
        self.power = pwr
                
    def checkDead(self):
        return self.health>0

    def printInfo(self):
        print(self.getInfo())

    def getInfo(self):
        info = "{} - hp, {} - spd, {} - pwr\n assigned to group {}\n"
        return info.format(self.health,self.speed,self.power,self.groupid)


class DeadBody(Unit):
    def __init__(self, hp, spd, pwr, value, damagedPoints):
        assert (hp<=0), "can not create a corpse from a dead unit"
        Unit.__init__(self, 0, -1, 0, 0)
        self.damagedPoints = damagedPoints-hp
        if self.damagedPoints>20:
            self.corpseType="dust"
        elif self.damagedPoints>10:
            self.corpseType="skeleton"
        else:
            self.corpseType="body"
        self.corpsValue = value + spd + pwr
        self.alive = False
    
    def getInfo(self):
        info=Unit.getInfo(self)
        info+="all that remains of the unit is " + self.corpseType + " \n "
        info+="and its value is " + self.value + " \n "
        return info


class PossessedCreature(Unit):
    def __init__(self, hp, spd, pwr, pb):
        assert (hp>0), "can not create a alive unit from hp<=0"
        
        Unit.__init__(self, hp, 0, spd, pwr)
        self.alive = True
        self.possessed = True
        self.сreatureType="None"
        self.possessedBonus = pb
        
    def getInfo(self):
        info=Unit.getInfo(self)
        info+="possessed being - " + self.сreatureType + "\n"
        info+="with " + str(self.possessedBonus) + " posees bonus\n"
        return info


class Necromancer(PossessedCreature):
    def __init__(self, hp, spd, pwr, pb, armor, mp):
        PossessedCreature.__init__(self, hp, spd, pwr, pb)
        self.сreatureType="Human"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        self.magicPoints = mp
        
    def getInfo(self):
        info=PossessedCreature.getInfo(self)
        info+="it also wears armor - " + str(self.armorLevel) + " level\n"
        info+="and containce - " + str(self.magicPoints) + " magic points\n"
        return info

    def getValue(self):
        return self.armorLevel+self.magicPoints+self.possessedBonus


class Skeleton(PossessedCreature):
    def __init__(self, hp, spd, pwr, pb, armor, ammo, wlvl):
        PossessedCreature.__init__(self, hp, spd, pwr, pb)
        self.сreatureType="Skeleton"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        assert (ammo>=0), "can not have an negative amount of ammo"
        self.ammo = ammo
        assert (wlvl>=0), "can not have an negative level of weapon"
        self.weaponLevel=wlvl
        
    def getInfo(self):
        info=PossessedCreature.getInfo(self)
        info+="it also wears armor - " + str(self.armorLevel) + " level\n"
        info+="have " + str(self.weaponLevel) + " level weapon\n"
        info+="and have " + str(self.ammo) + " bones to throw\n"
        return info

    def haveAmmo(self):
        return self.ammo>0

    def getValue(self):
        return self.armorLevel+self.ammo+self.possessedBonus+self.weaponLevel


class Zombie(PossessedCreature):
    def __init__(self, hp, spd, pwr, pb, armor, wlvl):
        PossessedCreature.__init__(self, hp, spd, pwr, pb)
        self.сreatureType="Zombie"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        assert (wlvl>=0), "can not have an negative level of weapon"
        self.weaponLevel=wlvl
        
    def getInfo(self):
        info=PossessedCreature.getInfo(self)
        info+="it also wears armor - " + str(self.armorLevel) + " level\n"
        info+="and have " + str(self.weaponLevel) + " level weapon\n"
        return info

    def getValue(self):
        return self.armorLevel+self.possessedBonus    


class SaneCreature(Unit):
    def __init__(self, hp, grp, spd, pwr):
        assert (hp>0), "can not create a alive unit from hp<=0"
        assert (grp>0), "Sane Creature can not be in <=0 team"
        Unit.__init__(self, hp, grp, spd, pwr)
        self.alive = True
        self.possessed = False
        self.сreatureType="None"
        
    def getInfo(self):
        info=Unit.getInfo(self)
        info+="Sane being - " + self.сreatureType + "\n"
        return info


class Soldier(SaneCreature):
    def __init__(self, hp, grp, spd, pwr, armor, wlvl, ammo):
        SaneCreature.__init__(self, hp, grp, spd, pwr)
        self.сreatureType="Human"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        assert (ammo>=0), "can not have an negative amount of ammo"
        self.ammo = ammo
        assert (wlvl>=0), "can not have an negative level of weapon"
        self.weaponLevel=wlvl

    def haveAmmo(self):
        return self.ammo>0
        
    def getInfo(self):
        info=SaneCreature.getInfo(self)
        info+="he also wears armor - " + str(self.armorLevel) + " level\n"
        info+="have " + str(self.weaponLevel) + " level weapon\n"
        info+="and have " + str(self.ammo) + " arrows\n"
        return info

    def getValue(self):
        return self.armorLevel+self.weaponLevel+self.ammo

class Inventor(SaneCreature):
    def __init__(self, hp, grp, spd, pwr, armor, exp, money, retr):
        SaneCreature.__init__(self, hp, grp, spd, pwr)
        self.сreatureType="Human"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        assert (exp>=0), "can not have an negative amount of exp"
        self.campExperince = exp
        assert (money>=0), "can not have an negative level of money"
        self.moneyAmount = money
        self.retreats = retr
        
    def getInfo(self):
        info=SaneCreature.getInfo(self)
        info+="he also wears armor - " + str(self.armorLevel) + " level\n"
        info+="have " + str(self.campExperince) + " ex points\n"
        info+="and " + str(self.moneyAmount) + " gold coins\n"
        if self.retreats:
            info+="he is reatriting to camp\n"
        return info

    def getValue(self):
        return self.armorLevel+self.exp+self.money

class Horse(SaneCreature):
    def __init__(self, hp, grp, spd, pwr, armor):
        SaneCreature.__init__(self, hp, grp, spd, pwr)
        self.сreatureType="Horse"
        assert (armor>=0), "can not have an negative level armor"
        self.armorLevel = armor
        
    def getInfo(self):
        info=SaneCreature.getInfo(self)
        info+="it also wears armor - " + str(self.armorLevel) + " level\n"
        return info

    def getValue(self):
        return self.armorLevel
