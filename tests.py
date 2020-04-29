from creatures import *


def test_creatures_init_system(hp, shield):
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


def test_creatures_hit_system(hp, shield, hit, expected_hp, expected_shield, expected_is_dead):
    for i in range(len(hp)):
        unit = Unit(hp[i], shield[i])
        unit.hit(hit[i])
        assert unit.hp == expected_hp[i], "ошибка в рачёте здоровья при ударе"
        assert unit.shield == expected_shield[i], "ошибка в рачёте щитов при ударе"
        assert unit.is_dead() == expected_is_dead[i], "ошибка в рачёте смерти при ударе"


def test_creatures_type_and_features_system():
    unit = Unit()
    unit_type = set()
    unit_type.add(unit.type)

    soldiers = list()
    soldiers.append(Soldier("Bob0", "MasterBob"))
    soldiers.append(LeaderSoldier("Bob1", "MasterBob"))
    soldiers.append(CursedSoldier("Bob2", "MasterBob"))
    soldiers.append(BlessedSoldier("Bob3", "MasterBob"))
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


def test_creatures_features_exceptions():
    s_types_with_features = [LeaderSoldier, CursedSoldier, BlessedSoldier]
    for s in s_types_with_features:
        try:
            unit = s("Bob", "MasterBob", 1, 0, -1)
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


def test_creatures():
    hp = [0, 0, -100, 69, 42]
    shield = [0, 100, 0, -1, -100]
    test_creatures_init_system(hp, shield)

    hp = [10, 123, 1000, 69, 1]
    shield = [100, 0, 0, 42, 0]
    hit = [0, 122, 1, 13, 1]
    expected_hp = [10, 1, 999, 69, 0]
    expected_shield = [100, 0, 0, 29, 0]
    expected_is_dead = [False, False, False, False, True]
    test_creatures_hit_system(hp, shield, hit, expected_hp, expected_shield, expected_is_dead)

    test_creatures_type_and_features_system()

    test_creatures_features_exceptions()


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
            try_sub = sub('invalid', 'invalid')
        except ValueError:
            ...
        else:
            raise ValueError("Тест на отрицательные фичи не выдал ошибок")


def run_tests():
    try:
        test_creatures()
        test_act()
    except Exception:
        print("Ошибка тестирования системы")
    else:
        print("Тесты пройдены успешно")
