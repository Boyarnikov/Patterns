class Act:
    types = ['atk', 'def', 'heal']

    def __init__(self, string='atk'):
        if string in Act.types:
            self.type = string
        else:
            raise ValueError("Неверный тип действия")


class Unit:
    default_hp = 3
    default_shield = 0

    def __init__(self, hp=default_hp, shield=default_shield):
        if hp <= 0:
            raise ValueError("Создаётся существо с неположительным здоровьем")
        self.hp = hp
        if shield < 0:
            raise ValueError("Созаётся существо с отрицательными щитами")
        self.shield = shield
        self.atk_slots = list()
        self.def_slots = list()
        self.profs = list()
        self.type = None

    def is_dead(self):
        return self.hp <= 0

    def hit(self, amount=1):
        self.hp -= max(amount - self.shield, 0)
        self.shield = max(0, self.shield - amount)

    def set_profs(self, atk=0.50, defence=0.50, heal=0.50):
        self.profs = dict()
        self.profs['atk'] = atk
        self.profs['def'] = defence
        self.profs['heal'] = heal

    def set_atk(self, stats=[None]):
        self.atk_slots = list()
        for i in stats:
            self.atk_slots(Act(i))

    def set_def(self, stats=[None]):
        self.def_slots = list()
        for i in stats:
            self.def_slots(Act(i))

    def get_data_string(self):
        info = ''
        info += f"Это существо имеет {self.hp} здоровья,\n"
        info += f"{self.shield} щитов, его профессионализм: {self.profs}\n"
        info += f"его скилы защиты: {self.def_slots}; нападения {self.atk_slots}\n"
        return info


class Soldier(Unit):
    def __init__(self, name, master, hp=Unit.default_hp, shield=Unit.default_shield):
        Unit.__init__(self, hp, shield)
        self.name = name
        self.master = master
        self.type = 'soldier'
        self.feature = None

    def get_data_string(self):
        info = Unit.get_data_string(self)
        info += f"Солдат {self.name} армии {self.master}\n"
        return info


class LeaderSoldier(Soldier):
    default_init_points = 1

    def __init__(self, name, master, hp=Unit.default_hp, shield=Unit.default_shield, init_points=default_init_points):
        Soldier.__init__(self, name, master, hp, shield)
        if init_points <= 0:
            raise ValueError("Созаётся существо с неположительными очками инициативы")
        self.init_points = init_points
        self.feature = 'leader'

    def get_data_string(self):
        info = Soldier.get_data_string(self)
        info += f"Его лидерские качества дают армии {self.init_points} очков действий\n"
        return info


class Curse:
    types = ['dead', 'damaged', 'heal', 'atk', 'def']
    deals = ['hit_to_self', 'hit_to_teammate', 'hit_to_all', 'heal_enemy']

    def __init__(self, set_type=None, set_deals=None):
        if set_type in Curse.types and set_deals in Curse.deals:
            self.type = set_type
            self.deals = set_deals
        else:
            raise ValueError("Неверный тип проклятья")


class CursedSoldier(Soldier):
    default_double_luck = 0.0

    def __init__(self, name, master, hp=Unit.default_hp, shield=Unit.default_shield, double_luck=default_double_luck):
        Soldier.__init__(self, name, master, hp, shield)
        if not (0 <= double_luck <= 1):
            raise ValueError("Созаётся существо с некорректным значением удачи")
        self.double_luck = double_luck
        self.curse = None
        self.feature = 'cursed'

    def set_curse(self, curse):
        self.curse = curse

    def get_data_string(self):
        info = Soldier.get_data_string(self)
        info += f'Этот солдат проклят, поэтому при событии "{self.curse.type}"\n'
        info += f'произойдёт событие "{self.curse.deal}"\n'
        info += f'Сделка с дьяволом дала ему {int(self.double_luck * 100)}% шанс повторного выполнения действия\n'
        return info


class Bless:
    types = ['def', 'atk', 'heal']
    deals = ['heal_to_self', 'heal_to_teammate', 'heal_to_all', 'hit_enemy']

    def __init__(self, set_type=None, set_deals=None):
        if set_type in Bless.types and set_deals in Bless.deals:
            self.type = set_type
            self.deals = set_deals
        else:
            raise ValueError("Неверный тип благословления")


class BlessedSoldier(Soldier):
    default_luck = 0.0

    def __init__(self, name, master, hp=Unit.default_hp, shield=Unit.default_shield, luck=default_luck):
        Soldier.__init__(self, name, master, hp, shield)
        if not (0 <= luck <= 1):
            raise ValueError("Созаётся существо с некорректным значением удачи")
        self.luck = luck
        self.bless = None
        self.feature = 'blessed'

    def set_curse(self, bless):
        self.bless = bless

    def get_data_string(self):
        info = Soldier.get_data_string(self)
        info += f'Этот солдат благословлён, поэтому при событии "{self.curse.type}"\n'
        info += f'произойдёт событие "{self.curse.deal}"\n'
        info += f'с вероятностью {int(self.double_luck * 100)}%\n'
        return info


class Monster(Unit):
    def __init__(self, hp=Unit.default_hp, shield=Unit.default_shield):
        Unit.__init__(self, hp, shield)
        self.type = 'monster'
        self.feature = None

    def get_data_string(self):
        info = Unit.get_data_string(self)
        info += f"Монстр армии зла\n"
        return info


class LeaderMonster(Monster):
    default_init_points = 1

    def __init__(self, hp=Unit.default_hp, shield=Unit.default_shield, init_points=default_init_points):
        Monster.__init__(self, hp, shield)
        if init_points <= 0:
            raise ValueError("Созаётся существо с неположительными очками инициативы")
        self.init_points = init_points
        self.feature = 'leader'

    def get_data_string(self):
        info = Monster.get_data_string(self)
        info += f"Его лидерские качества дают армии {self.init_points} очков действий\n"
        return info
