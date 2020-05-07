from actions import *


class Unit:
    default_hp = 3
    default_shield = 0

    def __init__(self, hp=default_hp, shield=default_shield):
        if hp <= 0:
            raise ValueError("Создаётся существо с неположительным здоровьем")
        self.hp = hp
        self.max_hp = hp
        if shield < 0:
            raise ValueError("Созаётся существо с отрицательными щитами")
        self.shield = shield
        self.atk_slots = list()
        self.def_slots = list()
        self.set_profs(dict())
        self.type = None
        self.feature = None

    def is_dead(self):
        return self.hp <= 0

    def hit(self, amount=1):
        if amount < 0:
            raise ValueError("Отрицательный урон по юниту")
        self.hp -= max(amount - self.shield, 0)
        self.shield = max(0, self.shield - amount)

    def heal(self, amount=1):
        if amount < 0:
            raise ValueError("Отрицательное лечение по юниту")
        self.hp = min(self.hp + amount, self.max_hp)

    def set_profs(self, set_profs):
        self.profs = dict()
        for act in ACT_TYPES:
            if act in set_profs.keys():
                if not 0 <= set_profs[act] <= 1:
                    raise ValueError("Неверное значение професиональности передано")
                self.profs[act] = set_profs[act]
            else:
                self.profs[act] = 0

    def get_profs(self):
        d = self.profs.copy()
        return d

    def set_atk(self, stats=[None]):
        self.atk_slots = list()
        for i in stats:
            self.atk_slots(Act(i))

    def get_atk(self):
        return self.atk_slots.copy()

    def set_def(self, stats=[None]):
        self.def_slots = list()
        for i in stats:
            self.def_slots(Act(i))

    def get_def(self):
        return self.def_slots.copy()

    def __str__(self):
        info = ''
        info += f"Это существо имеет {self.hp} здоровья,\n"
        info += f"{self.shield} щитов, его профессионализм: {self.profs}\n"
        info += f"его скилы защиты: {self.def_slots}; нападения: {self.atk_slots}\n"
        return info


class Soldier(Unit):
    def __init__(self, name, hp=Unit.default_hp, shield=Unit.default_shield):
        Unit.__init__(self, hp, shield)
        self.name = name
        self.type = 'soldier'
        self.feature = None

    def __str__(self):
        info = Unit.__str__(self)
        info += f"Солдат {self.name}\n"
        return info


class LeaderSoldier(Soldier):
    default_init_points = 1

    def __init__(self, name, hp=Unit.default_hp, shield=Unit.default_shield, init_points=default_init_points):
        Soldier.__init__(self, name, hp, shield)
        if init_points <= 0:
            raise ValueError("Созаётся существо с неположительными очками инициативы")
        self.init_points = init_points
        self.feature = 'leader'

    def __str__(self):
        info = Soldier.__str__(self)
        info += f"Его лидерские качества дают армии {self.init_points} очков действий\n"
        return info


class CursedSoldier(Soldier):
    default_double_luck = 0.0

    def __init__(self, name, hp=Unit.default_hp, shield=Unit.default_shield, double_luck=default_double_luck):
        Soldier.__init__(self, name, hp, shield)
        if not (0 <= double_luck <= 1):
            raise ValueError("Созаётся существо с некорректным значением удачи")
        self.double_luck = double_luck
        self.curse = None
        self.feature = 'cursed'

    def set_curse(self, curse):
        self.curse = curse

    def __str__(self):
        info = Soldier.__str__(self)
        info += f'Этот солдат проклят, поэтому при событии "{self.curse.type}"\n'
        info += f'произойдёт событие "{self.curse.deal}"\n'
        info += f'Сделка с дьяволом дала ему {int(self.double_luck * 100)}% шанс повторного выполнения действия\n'
        return info


class BlessedSoldier(Soldier):
    default_luck = 0.0

    def __init__(self, name, hp=Unit.default_hp, shield=Unit.default_shield, luck=default_luck):
        Soldier.__init__(self, name, hp, shield)
        if not (0 <= luck <= 1):
            raise ValueError("Созаётся существо с некорректным значением удачи")
        self.luck = luck
        self.bless = None
        self.feature = 'blessed'

    def set_bless(self, bless):
        self.bless = bless

    def __str__(self):
        info = Soldier.__str__(self)
        info += f'Этот солдат благословлён, поэтому при событии "{self.curse.type}"\n'
        info += f'произойдёт событие "{self.curse.deal}"\n'
        info += f'с вероятностью {int(self.double_luck * 100)}%\n'
        return info


class Monster(Unit):
    def __init__(self, name='nameless', hp=Unit.default_hp, shield=Unit.default_shield):
        Unit.__init__(self, hp, shield)
        self.type = 'monster'
        self.feature = None
        self.name = name

    def __str__(self):
        info = Unit.__str__(self)
        info += f"Монстр {self.name}\n"
        return info


class LeaderMonster(Monster):
    default_init_points = 1

    def __init__(self, name='nameless', hp=Unit.default_hp, shield=Unit.default_shield, init_points=default_init_points):
        Monster.__init__(self, name, hp, shield)
        if init_points <= 0:
            raise ValueError("Созаётся существо с неположительными очками инициативы")
        self.init_points = init_points
        self.feature = 'leader'

    def __str__(self):
        info = Monster.__str__(self)
        info += f"Его лидерские качества дают армии {self.init_points} очков действий\n"
        return info
