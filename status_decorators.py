EXHAUSTED_FACTOR = 0.5
WEAKENED_FACTOR = 0.5
STRONGER_FACTOR = 2
PROTECTED_FACTOR = 2


class StatusDecorator:
    status_name = 'none'

    def __init__(self, unit):
        self.unit = unit
        self.status_name = self.__class__.status_name

    def __getattr__(self, atr):
        unit = self
        while isinstance(unit, StatusDecorator):
            unit = unit.unit
        return unit.__getattribute__(atr)

    def redecorate(self):
        if isinstance(self.unit, StatusDecorator):
            return self.unit.redecorate()
        else:
            return self.unit

    def __str__(self):
        info = self.unit.__str__()
        info += f"Под воздействием {self.name}\n"
        return info

    def get_statuses(self):
        statuses = self.unit.get_statuses()
        statuses.append(self.status_name)
        return statuses


class StatusExhausted(StatusDecorator):
    exhausted_factor = EXHAUSTED_FACTOR
    status_name = 'exhausted'

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['def'] = d['def'] * self.exhausted_factor
        return d


class StatusProtected(StatusDecorator):
    protected_factor = PROTECTED_FACTOR
    status_name = 'protected'

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['def'] = 1 - ((1 - d['def']) * (1 / self.protected_factor))
        return d


class StatusWeakened(StatusDecorator):
    weakened_factor = EXHAUSTED_FACTOR
    status_name = 'weakened'

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['atk'] = d['atk'] * self.weakened_factor
        return d


class StatusStronger(StatusDecorator):
    stronger_factor = STRONGER_FACTOR
    status_name = 'stronger'

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['atk'] = 1 - ((1 - d['atk']) * (1 / self.stronger_factor))
        return d


class StatusInvincible(StatusDecorator):
    status_name = 'invincible'

    def hit(self, amount=1):
        return


STATUSES = [StatusExhausted, StatusProtected, StatusWeakened, StatusStronger, StatusInvincible]
STATUS_DICT = dict()
for status in STATUSES:
    STATUS_DICT[status.status_name] = status
