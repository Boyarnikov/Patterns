import units
import unit_structures
import fight_structure
import tests
import random as r
import actions_const

ACT_GENERATOR = ['atk', 'atk', 'atk', 'atk', 'def', 'heal']
tests.run_tests()

A = 0.0
for testes in range(1):
    units_list = list()
    for index in range(8):
        init = max(0, r.randint(-8, 2))
        if init > 0:
            units_list.append(units.LeaderSoldier(str(index), r.randint(1, 3), r.randint(1, 2), init))
        else:
            units_list.append(units.Soldier(str(index), r.randint(1, 5), r.randint(1, 3)))
        units_list[index].set_profs(dict(zip(actions_const.ACT_TYPES, [round(r.random(), 2) for i in range(3)])))
        units_list[index].set_atk(r.sample(ACT_GENERATOR, r.randint(1, 3)))
        units_list[index].set_def(r.sample(ACT_GENERATOR, r.randint(1, 3)))

    g = [unit_structures.Group('Master1'), unit_structures.Group('Master2')]

    for index in range(8):
        print(units_list[index])
        g[index % 2].add_item(units_list[index])

    iterate = 0
    while not g[0].is_dead() and not g[1].is_dead() and iterate < 100:
        iterate += 1
        f = fight_structure.Fight(g[iterate % 2], g[(iterate + 1) % 2])
        f.iterate()
        logs = f.end_fight()
        for log in logs:
           print(log.__dict__)
        print()

    if g[0].is_dead():
        print('team 1 win')
        A += 1
    elif g[1].is_dead():
        print('team 0 win')
        ...
    else:
        A += 0.5
