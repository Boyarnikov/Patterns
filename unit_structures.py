class Group:
    starting_init_points = 3
    default_shield = 0

    def __init__(self, master):
        self.master = str(master)
        self.init_points = Group.starting_init_points
        self.units = list()

    def add_unit(self, unit):
        if unit.type is not None:
            if unit.feature == 'leader':
                self.init_points += unit.init_points
        self.units.append(unit)

    def remove_unit(self, unit):
        try:
            if unit.type is not None:
                if unit.feature == 'leader':
                    self.init_points -= unit.init_points
            self.units.remove(unit)
        except ValueError:
            raise ValueError("Попытка удалить юнита, не находящегося в группе")

    def remove_index(self, index):
        if 0 <= index <= len(self.units):
            unit = self.units[index]
            if unit.type is not None:
                if unit.feature == 'leader':
                    self.init_points -= unit.init_points
            self.units.pop(index)
        else:
            raise ValueError("Номер удаляемого юнита не в рамках листа")

    def clear_dead(self):
        for index in range(len(self.units) - 1, -1, -1):
            if self.units[index].is_dead():
                self.remove_index(index)

    def is_dead(self):
        return len(self.units) == 0

    def __str__(self):
        info = ''
        for unit in self.units:
            info += str(unit) + '\n'
        return info