import units
import units_const
import actions
import actions_const
import unit_structures
import random as r


def get_random_prof(potential=3):
    size = len(actions_const.ACT_TYPES)
    percents = 100 + (potential - 3) * (size * 4)
    percents = min(percents, size * 100)
    profs = list()
    for i in range(size - 1):
        profs.append(r.randint(1, min(percents//(size - i) * 2, 100)))
        percents -= profs[i]
    profs.append(min(percents, 100))
    r.shuffle(profs)
    for i in range(size):
        profs[i] /= 100
        profs[i] = min(profs[i], 1)
    profs = dict(zip(actions_const.ACT_TYPES, profs))
    return profs


def get_random_act_list(potential=3, profs=dict()):
    size = r.randint(1, potential//2)
    if len(profs.keys()) != len(actions_const.ACT_TYPES):
        profs = dict(zip(actions_const.ACT_TYPES, [1 for i in range(len(actions_const.ACT_TYPES))]))

    acts = list()
    for act in actions_const.ACT_TYPES:
        assert act in profs.keys(), "словарь profs не содержит все действия"
        acts.extend([act] * int(profs[act] * 100 // 10))

    r.shuffle(acts)
    acts = acts[:size]
    return acts


def get_random_unit(name, tier=0, feature='random'):
    if feature == 'random':
        if r.random() > 1 / (tier + 1):
            feature = r.choice(units_const.SOLDIER_FEATURES)
        else:
            feature = 'none'

    potential = r.randint(3, 5) + tier*2
    hp = (potential // 3) + r.randint(0, potential // 3)
    shields = r.randint(0, potential // 4)

    profs = get_random_prof(potential)
    act_atk = get_random_act_list(potential, profs)
    act_def = get_random_act_list(potential, profs)

    assert feature in units_const.SOLDIER_FEATURES, "Попытка создать юнита с инвалидной фичой " + feature
    if feature == 'none':
        unit = units.Soldier(name, hp, shields)
    elif feature == 'cursed':
        unit = units.CursedSoldier(name, hp, shields)
        unit.double_luck = 1
    elif feature == 'blessed':
        unit = units.BlessedSoldier(name, hp, shields)
        unit.luck = 1
    elif feature == 'leader':
        unit = units.LeaderSoldier(name, hp, shields, 1 + r.randint(0, potential // 8))

    unit.set_profs(profs)
    unit.set_atk(act_atk)
    unit.set_def(act_def)

    return unit
