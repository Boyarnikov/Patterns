import units
import unit_structures
import rounds_structure
import tests
import random as r
import actions_const
import render

my_render = render.Render()

ACT_GENERATOR = ['atk']
tests.run_tests()

A = 0.0

units_list = list()
for index in range(4):
    init = max(0, r.randint(-8, 2))

    if init > 0:
        units_list.append(units.LeaderSoldier(str(index), r.randint(1, 12), 0, init))
    elif init > -2:
        units_list.append(units.CursedSoldier(str(index), r.randint(1, 12), 0))
        units_list[index].double_luck = 1
    elif init > -4:
        units_list.append(units.CursedSoldier(str(index), r.randint(1, 12), 0))
        units_list[index].double_luck = 1
    else:
        units_list.append(units.Soldier(str(index), r.randint(1, 12), 0))

    units_list[index].set_profs(dict(zip(actions_const.ACT_TYPES, [1 for i in range(3)])))
    units_list[index].set_atk(r.sample(ACT_GENERATOR, r.randint(0, 1)))
    units_list[index].set_def(r.sample(ACT_GENERATOR, r.randint(0, 1)))

armies = [unit_structures.Army(), unit_structures.Army()]
armies[0].add_item(unit_structures.Group('Master1'))
armies[0].add_item(unit_structures.Group('Master2'))
armies[1].add_item(unit_structures.Group('Monster1'))
armies[1].add_item(unit_structures.Group('Monster2'))

for index in range(len(units_list)):
    print(units_list[index])
    armies[index % 2].items[index // 2 % 2].add_item(units_list[index])

r = rounds_structure.Round(armies[0], armies[1])
r.iterate()
logs = r.end_round()
my_render.append_data(logs)

my_render.render_data()
