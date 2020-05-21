class DataLog:
    time = 0.0001

    def __init__(self):
        self.type = None
        self.time = self.__class__.time


class LogRoundInit(DataLog):
    def __init__(self):
        DataLog.__init__(self)
        self.type = 'output_init'


class LogRoundEnd(DataLog):
    def __init__(self):
        DataLog.__init__(self)
        self.type = 'output_end'


class LogActionInfo(DataLog):
    def __init__(self, master, name, act):
        DataLog.__init__(self)
        self.type = 'act_info'
        self.master = master
        self.act = act
        self.name = name


class LogStatusInfo(DataLog):
    def __init__(self, master, name, status, whom):
        DataLog.__init__(self)
        self.type = 'status_info'
        self.master = master
        self.name = name
        self.status = status
        self.whom = whom


class LogHitInfo(DataLog):
    def __init__(self, master, name, hit, whom):
        DataLog.__init__(self)
        self.type = 'hit_info'
        self.master = master
        self.name = name
        self.hit = hit
        self.whom = whom


class LogDeathInfo(DataLog):
    def __init__(self, master, name):
        DataLog.__init__(self)
        self.type = 'death_info'
        self.master = master
        self.name = name


class LogUnitInfo(DataLog):
    def __init__(self, master, name, hp, shield, unit_type, feature, statuses):
        DataLog.__init__(self)
        self.master = master
        self.name = name
        self.type = 'unit_info'
        self.hp = hp
        self.shield = shield
        self.unit_type = unit_type
        self.feature = feature
        self.statuses = statuses


class LogFightInfo(DataLog):
    def __init__(self, master_atk, num_atk, master_def, num_def):
        DataLog.__init__(self)
        self.type = 'fight_info'
        self.master_atk = master_atk
        self.master_def = master_def
        self.num_atk = num_atk
        self.num_def = num_def


class LogRoundInfo(DataLog):
    def __init__(self, players_num, enemies_num):
        DataLog.__init__(self)
        self.type = 'round_info'
        self.players_num = players_num
        self.enemies_num = enemies_num


class LogPlayerInfo(DataLog):
    def __init__(self, player, money, size):
        DataLog.__init__(self)
        self.type = 'player_info'
        self.player = player
        self.money = money
        self.size = size


class LogAuctionInit(DataLog):
    def __init__(self):
        DataLog.__init__(self)
        self.type = 'auction_init'


class LogAuctionTime(DataLog):
    def __init__(self, time):
        DataLog.__init__(self)
        self.type = 'auction_time'
        self.time = time


class LogAuctionEnd(DataLog):
    def __init__(self):
        DataLog.__init__(self)
        self.type = 'auction_end'


class LogAuctionBet(DataLog):
    def __init__(self, player, num, money):
        DataLog.__init__(self)
        self.type = 'auction_bet'
        self.player = player
        self.num = num
        self.money = money


class LogAuctionReject(DataLog):
    def __init__(self, player):
        DataLog.__init__(self)
        self.type = 'auction_rj'
        self.player = player


class LogAuctionResult(DataLog):
    def __init__(self, d):
        DataLog.__init__(self)
        self.type = 'auction_res'
        self.res = d.copy()


class LogAuctionUnit(DataLog):
    def __init__(self, num, hp, shield, unit_type, feature, name, atk_slots, def_slots, profs, init_p, curse, bless):
        DataLog.__init__(self)
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
            self.curse = curse.make_list()
        if bless is not None:
            self.bless = bless.make_list()


class LogPlayerAdd(DataLog):
    def __init__(self, player):
        DataLog.__init__(self)
        self.type = 'player_add'
        self.player = player


class LogPlayerRemove(DataLog):
    def __init__(self, player):
        DataLog.__init__(self)
        self.type = 'player_rm'
        self.player = player


class LogEnemyAdd(DataLog):
    def __init__(self, name, num):
        DataLog.__init__(self)
        self.type = 'enemy_add'
        self.num = num
        self.name = name


class LogGroupInfo(DataLog):
    def __init__(self, name, num):
        DataLog.__init__(self)
        self.type = 'group_info'
        self.num = num
        self.name = name


class InputLog:
    def __init__(self):
        self.type = None


class InputBet(InputLog):
    def __init__(self, player, money, num):
        InputLog.__init__(self)
        self.type = 'bet'
        self.player = player
        self.money = money
        self.num = num


class InputNewPlayer(InputLog):
    def __init__(self, player):
        InputLog.__init__(self)
        self.type = 'new'
        self.player = player
