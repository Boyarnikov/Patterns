import units


class Association:
    def __init__(self):
        self.items = list()

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        try:
            self.items.remove(item)
        except ValueError:
            raise ValueError("Попытка удалить обхект, не находящийся в асоциации")

    def remove_index(self, index):
        if 0 <= index <= len(self.items):
            self.items.pop(index)
        else:
            raise ValueError("Номер удаляемого объекта не в рамках асоциации")

    def clear_dead(self):
        for index in range(len(self.items) - 1, -1, -1):
            if self.items[index].is_dead():
                self.remove_index(index)

    def is_dead(self):
        return len(self.items) == 0

    def __str__(self):
        info = ''
        for item in self.items:
            info += str(item) + '\n'
        return info


class Group(Association):
    starting_init_points = 1

    def __init__(self, master):
        self.master = str(master)
        self.init_points = Group.starting_init_points
        Association.__init__(self)

    def add_item(self, unit):
        if unit.type is not None:
            if unit.feature == 'leader':
                self.init_points += unit.init_points
        Association.add_item(self, unit)

    def remove_item(self, unit):
        try:
            if unit.type is not None:
                if unit.feature == 'leader':
                    self.init_points -= unit.init_points
            Association.remove_item(self, unit)
        except AttributeError:
            raise AttributeError("Объект не имеет отрибутов Юнита")

    def remove_index(self, index):
        if 0 <= index <= len(self.items):
            unit = self.items[index]
            if unit.type is not None:
                if unit.feature == 'leader':
                    self.init_points -= unit.init_points
            Association.remove_index(self, index)
        else:
            raise ValueError("Номер удаляемого юнита не в рамках листа")

    def update_units(self):
        for i in range(len(self.items)):
            if not isinstance(self.items[i], units.Unit):
                self.items[i] = self.items[i].redecorate()
            self.items[i].shield = self.items[i].shield//2


class Army(Association):
    def clear_dead(self):
        for index in range(len(self.items) - 1, -1, -1):
            self.items[index].clear_dead()
            if self.items[index].is_dead():
                self.remove_index(index)
