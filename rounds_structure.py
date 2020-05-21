import random as r
import log_classes
import fight_structure


class Round:
    def __init__(self, first_army, second_army):
        self.first_army = first_army
        self.second_army = second_army
        self.logs = list()
        self.first_order = list()
        self.second_order = list()
        self.set_orders()

    def set_orders(self):  # устанавливает случайный порядок защиты-отаки

        order_first = [x for x in range(len(self.first_army.items))]
        order_second = [x for x in range(len(self.second_army.items))]
        r.shuffle(order_first)
        r.shuffle(order_second)
        self.logs.append(log_classes.LogRoundInit())
        first_names = [self.first_army.items[index].master for index in order_first]
        second_names = [self.second_army.items[index].master for index in order_second]
        self.logs.append(log_classes.LogRoundInfo(first_names, second_names))
        self.first_order = order_first
        self.second_order = order_second

    def make_fight(self, first_index, second_index, atk):

        if atk:
            f = fight_structure.Fight(self.first_army.items[first_index], self.second_army.items[second_index])
        else:
            f = fight_structure.Fight(self.second_army.items[second_index], self.first_army.items[first_index],)
        f.iterate()
        self.logs.extend(f.end_fight())

        if self.first_army.items[first_index].is_dead():
            if first_index in self.first_order:
                self.first_order.remove(first_index)
        if self.second_army.items[second_index].is_dead():
            if second_index in self.second_order:
                self.second_order.remove(second_index)

    def iterate(self):  # производит итерацию боя, обрабатывая логи и сохраняя их в self.logs
        enemy_index = 0
        for index in self.first_order:
            if self.first_army.is_dead() or self.second_army.is_dead():
                break
            if self.first_army.items[index].is_dead():
                continue
            if len(self.second_order) == 0:
                break
            enemy_index %= len(self.second_order)
            self.make_fight(index, self.second_order[enemy_index], True)
            enemy_index += 1

        enemy_index = 0
        for index in self.first_order:
            if self.first_army.is_dead() or self.second_army.is_dead():
                break
            if self.first_army.items[index].is_dead():
                continue
            if len(self.second_order) == 0:
                break
            enemy_index %= len(self.second_order)
            self.make_fight(index, self.second_order[enemy_index], False)
            enemy_index += 1

    def end_round(self):
        self.first_army.clear_dead()
        self.second_army.clear_dead()
        for group in self.first_army.items:
            group.update_units()
        for group in self.second_army.items:
            group.update_units()
        self.logs.append(log_classes.LogRoundEnd())
        return self.logs
