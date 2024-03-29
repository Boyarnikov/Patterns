from actions_const import *


class Act:
    types = ACT_TYPES

    def __init__(self, string='atk'):
        if string in Act.types:
            self.type = string
        else:
            raise ValueError("Неверный тип действия")

    def __str__(self):
        return 'ACT_'+self.type


class Curse:
    types = EVENTS_TYPES
    deals = BAD_DEALS
    whom = WHOM_ITEMS

    def __init__(self, set_type='none', set_deals='none', set_whom='none'):
        if (set_type in Curse.types and set_deals in Curse.deals and set_whom in Curse.whom) or \
                (set_type == 'none' and set_deals == 'none' and set_whom == 'none'):
            self.type = set_type
            self.deals = set_deals
            self.whom = set_whom
        else:
            raise ValueError("Неверный тип проклятья")

    def make_list(self):
        return [self.type, self.deals, self.whom]


class Bless:
    types = ACT_TYPES
    deals = GOOD_DEALS
    whom = WHOM_ITEMS

    def __init__(self, set_type='none', set_deals='none', set_whom='none'):
        if set_type in Bless.types and set_deals in Bless.deals and set_whom in Bless.whom or \
                (set_type == 'none' and set_deals == 'none' and set_whom == 'none'):
            self.type = set_type
            self.deals = set_deals
            self.whom = set_whom
        else:
            raise ValueError("Неверный тип благословления")

    def make_list(self):
        return [self.type, self.deals, self.whom]
