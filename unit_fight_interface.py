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
            if bless.deal == 'heal':
                self.logs.append(log.LogHitInfo('?master', name, -1, '?' + bless.whom))
            elif bless.deal in actions_const.STATUSES:
                self.logs.append(log.LogStatusInfo('?master', name, bless.deal, '?' + bless.whom))

    def handle_curse(self, curse, event, name):
        if event == curse.type:
            if curse.deal == 'hit':
                self.logs.append(log.LogHitInfo('?master', name, 1, '?' + curse.whom))
            elif curse.deal in actions_const.STATUSES:
                self.logs.append(log.LogStatusInfo('?master', name, curse.deal, '?' + curse.whom))

    def handle_act(self, act, unit):
        profs = unit.get_profs()
        times = 1
        if unit.feature == 'cursed':
            if self.act_success(unit.double_luck):
                times += 1
        for i in range(times):
            if self.act_success(profs[act]):
                self.logs.append(log.LogActionInfo('?master', act, unit.name))
                if unit.feature == 'blessed':
                    self.handle_bless(unit.bless, act, unit.name)

    def get_act_atk(self, unit):
        atk = unit.get_atk()
        for act in atk:
            self.handle_act(act, unit)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def get_act_def(self, unit):
        defence = unit.get_atk()
        for act in defence:
            self.handle_act(act, unit)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def hit(self, unit, hit):
        if hit > 0:
            unit.hit(hit)
            if unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'damaged', unit.name)
        if hit < 0:
            unit.heal(-hit)
            if unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'healed', unit.name)
        if unit.is_dead():
            log.LogDeathInfo('?master', unit.name)
            if unit.feature == 'cursed':
                self.handle_curse(unit.curse, 'dead', unit.name)
        send_logs = self.logs.copy()
        self.logs = list()
        return send_logs

    def shield(self, unit, shields):
        unit.shield += shields

    def set_status(self, unit, status):
        self.logs = list()
        return status_decorators.STATUS_DICT[status](unit)
