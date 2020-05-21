import units
import unit_structures
import rounds_structure
import tests
import random as r
import actions_const
import render
import random_generators
import tests


tests.run_tests()

my_render = render.Render()

units_list = list()
for index in range(8):
    units_list.append(random_generators.get_random_unit('Solder' + str(index), 1))
g = [unit_structures.Group('Master1'), unit_structures.Group('Master2')]

for index in range(8):
    print(units_list[index])
    g[index % 2].add_item(units_list[index])

armies = [unit_structures.Army(), unit_structures.Army()]
armies[0].add_item(unit_structures.Group('Master1'))
armies[0].add_item(unit_structures.Group('Master2'))
armies[1].add_item(unit_structures.Group('Monster1'))
armies[1].add_item(unit_structures.Group('Monster2'))

for index in range(len(units_list)):
    print(units_list[index])
    armies[index % 2].items[index // 2 % 2].add_item(units_list[index])

iterate = 0
while not armies[0].is_dead() and not armies[1].is_dead() and iterate < 100:
    r = rounds_structure.Round(armies[0], armies[1])
    r.iterate()
    logs = r.end_round()
    my_render.append_data(logs)
    my_render.render_data()
    for i in range(10):
        print()

if armies[0].is_dead():
    print('team 1 win')
elif armies[1].is_dead():
    print('team 0 win')
else:
    print('no one win')
