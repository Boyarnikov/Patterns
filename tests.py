from units import *
from unit_structures import *
from status_decorators import *


def test_units_init_system(hp, shield):
    unit = Unit()
    unit = Unit(10)
    unit = Unit(1, 0)
    unit = Unit(10000000000, 1000000000000)

    for i in range(len(hp)):
        try:
            unit = Unit(hp[i], shield[i])
        except ValueError:
            ...
        else:
            ValueError("Существо с отрицательными щитами или неположительным здоровьем создано")


def test_units_hit_system(hp, shield, hit, expected_hp, expected_shield, expected_is_dead):
    for i in range(len(hp)):
        unit = Unit(hp[i], shield[i])
        unit.hit(hit[i])
        assert unit.hp == expected_hp[i], "ошибка в рачёте здоровья при ударе"
        assert unit.shield == expected_shield[i], "ошибка в рачёте щитов при ударе"
        assert unit.is_dead() == expected_is_dead[i], "ошибка в рачёте смерти при ударе"


def test_units_type_and_features_system():
    unit = Unit()
    unit_type = set()
    unit_type.add(unit.type)

    soldiers = list()
    soldiers.append(Soldier("Bob0"))
    soldiers.append(LeaderSoldier("Bob1"))
    soldiers.append(CursedSoldier("Bob2"))
    soldiers.append(BlessedSoldier("Bob3"))
    s_types, s_features = set(), set()
    for i in soldiers:
        s_types.add(i.type)
        s_features.add(i.feature)
    assert (len(s_types) == 1) and (len(s_features) == 4), "Ошибка системы фич и типов для солдат"

    monsters = list()
    monsters.append(Monster())
    monsters.append(LeaderMonster())
    m_types, m_features = set(), set()
    for i in monsters:
        m_types.add(i.type)
        m_features.add(i.feature)
    assert (len(m_types) == 1) and (len(m_features) == 2), "Ошибка системы фич и типов для монстров"
    assert len(unit_type | m_types | s_types) == 3, "Ошибка именования типов"
    assert m_types.isdisjoint(s_types), "Ошибка именования типов"
    assert (unit.type not in m_types), "Ошибка именования типов"
    assert (unit.type not in s_types), "Ошибка именования типов"


def test_units_features_exceptions():
    s_types_with_features = [LeaderSoldier, CursedSoldier, BlessedSoldier]
    for s in s_types_with_features:
        try:
            unit = s("Bob", 1, 0, -1)
        except ValueError:
            ...
        else:
            raise ValueError("Тест на отрицательные фичи не выдал ошибок")
    m_types_with_features = [LeaderMonster]
    for m in m_types_with_features:
        try:
            unit = m(1, 0, -1)
        except ValueError:
            ...
        else:
            raise ValueError("Тест на отрицательные фичи не выдал ошибок")


def test_act():
    try:
        act = Act('invalid')
    except ValueError:
        ...
    else:
        raise ValueError("Тест на отрицательные фичи не выдал ошибок")
    test_subjects = [Bless, Curse]
    for sub in test_subjects:
        try:
            try_sub = sub('invalid', 'invalid', 'invalid')
        except ValueError:
            ...
        else:
            raise ValueError("Тест на отрицательные фичи не выдал ошибок")


def test_profs():
    unit = Unit()
    unit.set_profs(dict())

    profs = unit.get_profs()
    for i in profs.keys():
        assert profs[i] == 0, 'Базовый параметр професиональности не нулевой'
    profs = dict(zip(ACT_TYPES, [1 for i in range(len(ACT_TYPES))]))
    unit.set_profs(profs)

    stats = [[j for i in range(len(ACT_TYPES))] for j in [-1, 2, 'a']]

    for stat in stats:
        try:
            profs = dict(zip(ACT_TYPES, stat))
            unit.set_profs(profs)
        except ValueError:
            ...
        except TypeError:
            ...
        else:
            raise ValueError("Тест на некорректные значения не выдал ошибок")


def test_status_decorator():
    unit1 = Unit(10, 10)
    decorated = StatusDecorator(unit1)
    assert isinstance(decorated, StatusDecorator), 'Ошибка обёртки в декоратор статуса'
    unit2 = decorated.redecorate()
    assert isinstance(unit2, type(unit1)), 'Ошибка развёртки декоратора статуса'
    assert unit2 == unit1, 'Ошибка развёртки декоратора статуса'

    unit1 = Unit(10, 10)
    profs1 = dict(zip(ACT_TYPES, [0.5 for i in range(len(ACT_TYPES))]))
    unit1.set_profs(profs1)
    unit1 = StatusExhausted(unit1)
    unit1 = StatusWeakened(unit1)
    profs2 = dict(zip(ACT_TYPES, [0.5 for i in range(len(ACT_TYPES))]))
    profs2['atk'] = 0.25
    profs2['def'] = 0.25
    unit2.set_profs(profs2)
    assert unit1.get_profs() == unit2.get_profs(), 'Ошибка пересчёта професианализма внутри декораторов'

    unit1 = Unit(10, 10)
    profs1 = dict(zip(ACT_TYPES, [0.5 for i in range(len(ACT_TYPES))]))
    unit1.set_profs(profs1)
    unit1 = StatusStronger(unit1)
    unit1 = StatusProtected(unit1)
    profs2 = dict(zip(ACT_TYPES, [0.5 for i in range(len(ACT_TYPES))]))
    profs2['atk'] = 0.75
    profs2['def'] = 0.75
    unit2.set_profs(profs2)
    assert unit1.get_profs() == unit2.get_profs(), 'Ошибка пересчёта професианализма внутри декораторов'

    unit1 = Unit(10, 10)
    unit2 = StatusInvincible(unit1)
    unit2.hit(100000)
    unit2 = unit2.redecorate()
    assert unit1 == unit2, 'Ошибка пересчёта професианализма внутри декораторов'


def test_unit_base():
    hp = [0, 0, -100, 69, 42]
    shield = [0, 100, 0, -1, -100]
    test_units_init_system(hp, shield)

    hp = [10, 123, 1000, 69, 1]
    shield = [100, 0, 0, 42, 0]
    hit = [0, 122, 1, 13, 1]
    expected_hp = [10, 1, 999, 69, 0]
    expected_shield = [100, 0, 0, 29, 0]
    expected_is_dead = [False, False, False, False, True]
    test_units_hit_system(hp, shield, hit, expected_hp, expected_shield, expected_is_dead)


def test_units():
    test_unit_base()

    test_units_type_and_features_system()

    test_units_features_exceptions()

    test_act()

    test_profs()

    test_status_decorator()


def test_structures_groups():
    g = Group('Master')
    i_points = g.init_points
    unit1 = LeaderSoldier('Bob1', 1, 1, 10)
    g.add_unit(unit1)
    assert g.init_points - i_points == 10, 'Ошибка подсчёта очков инициативы группы'
    g.add_unit(unit1)
    assert g.init_points - i_points == 20, 'Ошибка подсчёта очков инициативы группы'
    g.add_unit(unit1)
    assert g.init_points - i_points == 30, 'Ошибка подсчёта очков инициативы группы'
    g.remove_unit(unit1)
    assert g.init_points - i_points == 20, 'Ошибка подсчёта очков инициативы группы'
    g.remove_index(0)
    assert g.init_points - i_points == 10, 'Ошибка подсчёта очков инициативы группы'
    unit1.hit(100000)
    g.clear_dead()
    assert g.is_dead(), 'Ошибка проверки гибели команды'
    assert g.init_points - i_points == 0, 'Ошибка подсчёта очков инициативы группы'


def test_structures():
    test_structures_groups()


def run_tests():
    try:
        test_units()
        test_structures()
    except Exception:
        print("Ошибка тестирования системы")
    else:
        print("Тесты пройдены успешно")
