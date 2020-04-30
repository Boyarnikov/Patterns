EXHAUSTED_FACTOR = 0.5
WEAKENED_FACTOR = 0.5
STRONGER_FACTOR = 2
PROTECTED_FACTOR = 2


class StatusDecorator:
    def __init__(self, unit):
        self.unit = unit

    def __getattr__(self, atr):
        return self.unit.__getattribute__(atr)

    def redecorate(self):
        if isinstance(self, StatusDecorator):
            return self.unit


class StatusExhausted(StatusDecorator):
    exhausted_factor = EXHAUSTED_FACTOR

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['def'] = d['def'] * self.exhausted_factor
        return d


class StatusProtected(StatusDecorator):
    protected_factor = PROTECTED_FACTOR

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['def'] = 1 - ((1 - d['def']) * (1 / self.protected_factor))
        return d


class StatusWeakened(StatusDecorator):
    weakened_factor = EXHAUSTED_FACTOR

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['atk'] = d['atk'] * self.weakened_factor
        return d


class StatusStronger(StatusDecorator):
    stronger_factor = STRONGER_FACTOR

    def get_profs(self):
        d = self.unit.get_profs().copy()
        d['atk'] = 1 - ((1 - d['atk']) * (1 / self.stronger_factor))
        return d


class StatusInvincible(StatusDecorator):
    def hit(self, amount=1):
        return
