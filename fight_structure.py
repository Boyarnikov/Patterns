from unit_fight_interface import *
import random as r
import actions_const
import log_classes


def cor_handle_log(f, log_data):  # первый элемент цепочки обязаностей
    cor_handle_log_act(f, log_data)


def cor_handle_log_act(f, log_data):  # обработчик act-ов
    if log_data.type in 'act_info':
        if log_data.master == '?master':
            log_data.master = f.find_master_by_unit_name(log_data.name)
        assert log_data.act in actions_const.ACT_TYPES, "Неверный тип действия в логе"
        f.logs.append(log_data)
        if log_data.act == "atk":
            cor_handle_log(f, log_classes.LogHitInfo('?master', log_data.name, 1, '?enemy'))
        elif log_data.act == "def":
            target = f.handle_units_names_find(log_data.name, '?self')
            f.interface.shield(f.find_unit_by_unit_name(target[0]), 1)
        elif log_data.act == "heal":
            cor_handle_log(f, log_classes.LogHitInfo('?master', log_data.name, -1, '?teammate'))
    else:
        cor_handle_log_hit(f, log_data)


def cor_handle_log_hit(f, log_data):  # обработчик hit-ов
    if log_data.type in 'hit_info':
        if log_data.master == '?master':
            log_data.master = f.find_master_by_unit_name(log_data.name)
        log_data.whom = f.handle_units_names_find(log_data.name, log_data.whom)
        f.logs.append(log_data)
        new_logs = list()
        for name in log_data.whom:
            unit = f.find_unit_by_unit_name(name)
            new_logs.extend(f.interface.hit(unit, log_data.hit))
            new_logs.append(f.make_unit_info_log(unit))
        for new_log in new_logs:
            cor_handle_log(f, new_log)
    else:
        cor_handle_log_status(f, log_data)


def cor_handle_log_status(f, log_data):  # обработчик наложения статусов
    if log_data.type in 'status_info':
        if log_data.master == '?master':
            log_data.master = f.find_master_by_unit_name(log_data.name)
        assert log_data.status in actions_const.STATUSES, "Неверный тип статуса в логе"
        log_data.whom = f.handle_units_names_find(log_data.name, log_data.whom)
        f.logs.append(log_data)
        for index in f.order_atk:
            if f.group_atk[index] in log_data.whom:
                f.group_atk[index] = f.interface.set_status(f.group_atk[index], log_data.status)
        for index in f.order_def:
            if f.group_def[index] in log_data.whom:
                f.group_def[index] = f.interface.set_status(f.group_def[index], log_data.status)
    else:
        cor_handle_log_death(f, log_data)


def cor_handle_log_death(f, log_data):  # обработчик наложения статусов
    if log_data.type in 'death_info':
        if log_data.master == '?master':
            log_data.master = f.find_master_by_unit_name(log_data.name)
        f.logs.append(log_data)
        for index in f.order_atk:
            if f.group_atk.items[index].name == log_data.name:
                f.order_atk.remove(index)
        for index in f.order_def:
            if f.group_def.items[index].name == log_data.name:
                f.order_def.remove(index)
    else:
        cor_handle_log_end(f, log_data)


def cor_handle_log_end(f, log_data):  # финальный обработчик статусов
    f.logs.append(log_data)


class Fight:
    def __init__(self, grout_atk, group_def):
        self.group_atk = grout_atk
        self.group_def = group_def
        self.logs = list()
        self.order_atk = list()
        self.order_def = list()
        self.interface = UnitFightInterface()
        self.set_orders()

    def set_orders(self):  # устанавливает случайный порядок защиты-отаки
        order_size = min(len(self.group_atk.items), self.group_atk.init_points)
        order_atk = [x for x in range(len(self.group_atk.items))]
        order_def = [x for x in range(len(self.group_def.items))]
        r.shuffle(order_atk)
        r.shuffle(order_def)
        self.order_atk = order_atk[:order_size]
        order_size = min(len(self.group_def.items), order_size)
        self.order_def = order_def[:order_size]
        self.logs.append(log_classes.LogRoundInit())
        self.logs.append(log_classes.LogFightInfo(self.group_atk.master, len(self.order_atk),
                                                  self.group_def.master, len(self.order_def),))
        for index in self.order_atk:
            self.logs.append(self.make_unit_info_log(self.group_atk.items[index]))
        for index in self.order_def:
            self.logs.append(self.make_unit_info_log(self.group_def.items[index]))

    def find_master_by_unit_name(self, name):  # ищет мастера по имени юнита
        for unit in self.group_atk.items:
            if unit.name == name:
                return self.group_atk.master
        for unit in self.group_def.items:
            if unit.name == name:
                return self.group_def.master

    def find_unit_by_unit_name(self, name):  # ищет юнита по его имени
        for unit in self.group_atk.items:
            if unit.name == name:
                return unit
        for unit in self.group_def.items:
            if unit.name == name:
                return unit

    def handle_units_names_find(self, unit_name, whom):  # возвращает список имён по запросу имён через whom = "?..."
        if not isinstance(whom, str):
            return []
        if whom[0] != '?':
            return [whom]
        unit = self.find_unit_by_unit_name(unit_name)
        my_group_names = list()
        enemy_group_names = list()

        for index in self.order_atk:
            my_group_names.append(self.group_atk.items[index].name)
        for index in self.order_def:
            enemy_group_names.append(self.group_def.items[index].name)

        if self.find_master_by_unit_name(unit_name) == self.group_def.master:
            my_group_names, enemy_group_names = enemy_group_names, my_group_names

        if whom[1:] == 'self':
            return [unit.name]
        elif whom[1:] == 'teammate':
            if len(my_group_names) == 0:
                return []
            return [r.choice(my_group_names)]
        elif whom[1:] == 'teammates':
            return my_group_names
        elif whom[1:] == 'enemy':
            if len(enemy_group_names) == 0:
                return []
            return [r.choice(enemy_group_names)]
        elif whom[1:] == 'enemies':
            return enemy_group_names
        elif whom[1:] == 'all':
            return my_group_names.extend(enemy_group_names)
        else:
            return []

    def handle_log(self, log_data):
        cor_handle_log(self, log_data)

    def iterate(self):  # производит итерацию боя, обрабатывая логи и сохраняя их в self.logs
        for index in self.order_def:
            unit = self.group_def.items[index]
            if unit.is_dead():
                continue
            logs = self.interface.get_act_def(unit)
            for log_data in logs:
                self.handle_log(log_data)
        for index in self.order_atk:
            unit = self.group_atk.items[index]
            if unit.is_dead():
                continue
            logs = self.interface.get_act_atk(unit)
            for log_data in logs:
                self.handle_log(log_data)

    def end_fight(self):
        self.group_atk.clear_dead()
        self.group_def.clear_dead()
        self.logs.append(log_classes.LogRoundEnd())
        return self.logs

    def make_unit_info_log(self, unit):
        master = self.find_master_by_unit_name(unit.name)
        return log_classes.LogUnitInfo(master, unit.name, unit.hp, unit.shield,
                                       unit.type, unit.feature, unit.get_statuses())
