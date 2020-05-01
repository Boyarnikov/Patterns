class DataLog:
    def __init__(self):
        self.type = None


class LogRoundInit(DataLog):
    def __init__(self):
        self.type = 'output_init'


class LogRoundEnd(DataLog):
    def __init__(self):
        self.type = 'output_end'


class LogActionInfo(DataLog):
    def __init__(self, master, act, name):
        self.type = 'act_info'
        self.master = master
        self.act = act
        self.unit_name = name


class LogStatusInfo(DataLog):
    def __init__(self, master, status, name):
        self.type = 'status_info'
        self.master = master
        self.status = status
        self.name = name


class LogHitInfo(DataLog):
    def __init__(self, master, hit, name):
        self.type = 'hit_info'
        self.master = master
        self.status = hit
        self.name = name


class LogDeathInfo(DataLog):
    def __init__(self, master, name):
        self.type = 'death_info'
        self.master = master
        self.name = name


class LogUnitInfo(DataLog):
    def __init__(self, master, hp, shield, unit_type, feature, name):
        self.type = 'unit_info'
        self.master = master
        self.hp = hp
        self.shield = shield
        self.unit_type = unit_type
        self.feature = feature
        self.name = name


class LogUnitInfo(DataLog):
    def __init__(self, master_atk, master_def):
        self.type = 'fight_info'
        self.master_atk = master_atk
        self.master_def = master_def


class LogRoundInfo(DataLog):
    def __init__(self, players_num, enemies_num):
        self.type = 'round_info'
        self.playerss_num = players_num
        self.enemies_num = enemies_num


class LogRoundInfo(DataLog):
    def __init__(self, player, money, size):
        self.type = 'player_info'
        self.player = player
        self.money = money
        self.size = size


class LogAuctionInit(DataLog):
    def __init__(self):
        self.type = 'auction_init'


class LogAuctionTime(DataLog):
    def __init__(self, time):
        self.type = 'auction_time'
        self.time = time


class LogAuctionEnd(DataLog):
    def __init__(self):
        self.type = 'auction_end'


class LogAuctionBet(DataLog):
    def __init__(self, player, num, money):
        self.type = 'auction_bet'
        self.player = player
        self.num = num
        self.money = money


class LogAuctionReject(DataLog):
    def __init__(self, player):
        self.type = 'auction_rj'
        self.player = player


class LogAuctionResult(DataLog):
    def __init__(self, d):
        self.type = 'auction_res'
        self.res = d.copy()


class LogAuctionUnit(DataLog):
    def __init__(self, num, hp, shield, unit_type, feature, name, atk_slots, def_slots, profs, init_p, curse, bless):
        self.type = 'auction_unit'
        self.num = num
        self.hp = hp
        self.shield = shield
        self.unit_type = unit_type
        self.feature = feature
        self.name = name
        self.atk_slots = atk_slots.copy()
        self.def_slots = def_slots.copy()
        self.profs = profs.copy()
        self.init_points = init_p
        if curse is not None:
            self.curse = [curse.types, curse.deals, curse.whom]
        if bless is not None:
            self.bless = [bless.types, bless.deals, bless.whom]


class LogPlayerAdd(DataLog):
    def __init__(self, player):
        self.type = 'player_add'
        self.player = player


class LogPlayerRemove(DataLog):
    def __init__(self, player):
        self.type = 'player_rm'
        self.player = player


class LogEnemyAdd(DataLog):
    def __init__(self, name, num):
        self.type = 'enemy_add'
        self.num = num
        self.name = name


class LogGroupInfo(DataLog):
    def __init__(self, name, num):
        self.type = 'group_info'
        self.num = num
        self.name = name
