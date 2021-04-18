import log_classes as log
import random as r
import actions_const
import status_decorators


class UnitFightInterface:
    def __init__(self):
        self.logs = list()

    def act_success(self, probability) -> bool:
        if not (0 <= probability <= 1):
            raise ValueError("Некорректным значением вероятности")
        else:
            result = r.random()
            if result < probability:
                return True
            return False

    def handle_bless(self, bless, act, name):
        if act == bless.type:
            if bless.deals == 'heal':
                self.logs.append(log.LogHitInfo('?master', name, -1, '?' + bless.whom))
            elif bless.deals in actions_const.STATUSES:
                self.logs.append(log.LogStatusInfo('?master', name, bless.deals, '?' + bless.whom))

    def handle_curse(self, curse, event, name):
        if event == curse.type:
            if curse.deals == 'hit':
                self.logs.append(log.LogHitInfo('?master', name, 1, '?' + curse.whom))
            elif curse.deals in actions_const.STATUSES:
                self.logs.append(log.LogStatusInfo('?master', name, curse.deals, '?' + curse.whom))

    def handle_act(self, act, unit):
        profs = unit.get_profs()
        times = 1
        if unit.feature == 'cursed':
            if self.act_success(unit.double_luck):
                times += 1
        for i in range(times):
            if self.act_success(profs[act]):
                self.logs.append(log.LogActionInfo('?master', unit.name, act))
                if unit.feature == 'blessed':
                    self.handle_bless(unit.bless, act, unit.name)

    def get_act_atk(self, unit):
        atk = unit.get_atk()
        for act in atk:
            self.handle_act(act.type, unit)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def get_act_def(self, unit):
        defence = unit.get_def()
        for act in defence:
            self.handle_act(act.type, unit)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def hit(self, unit, hit):
        if unit.is_dead():
            return list()
        if hit > 0:
            hp = unit.hp
            unit.hit(hit)
            if hp != unit.hp and unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'damaged', unit.name)
        if hit < 0:
            hp = unit.hp
            unit.heal(-hit)
            if hp != unit.hp and unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'healed', unit.name)
        if unit.is_dead():
            self.logs.append(log.LogDeathInfo('?master', unit.name))
            if unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'dead', unit.name)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def shield(self, unit, shields):
        if unit.is_dead():
            return list()
        unit.shield += shields
        return list()

    def set_status(self, unit, status):
        if status == 'none':
            if isinstance(unit, status_decorators.StatusDecorator):
                return unit.redecorate()
            else:
                return unit
        return status_decorators.STATUS_DICT[status](unit)
