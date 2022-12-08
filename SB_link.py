from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from SB_helpers import SB_pair


"""
Протокол
    name:cmd
Комманды:
    hx,y - выстрел по x,y
    rn - результат выстрела; n: 0 - мимо, 1 - попал, 2 - убил
    l - lose
    sx,y - палуба на x,y
    q - конец передачи палуб
    Q - готовность
# x,y,n - числа
# не отправляем новый запрос, пока не обработали старый

Файл с ключами:
    1 строка - имя игрока, ходящего первым
    2 строка - имя игрока, ходящего вторым
    3 строка - PubNub subscribe_key
    4 строка - PubNub publish_key
"""


class SB_attack_result:
    NONE = -1
    MISS = 0
    DAMAGE = 1
    KILL = 2


class SB_link:
    _DBGWAITFLAG = False

    channel_name = "seabattle"
    pubnub = None
    configfile = "keys.txt"
    myName = ''
    hisName = ''

    began = False
    slaveReady = False

    @classmethod
    def begin(cls, isMaster):
        cls.decks_recieved = []
        cls.isHeLose = False
        cls.isILose = False
        cls.attack_result = SB_attack_result.NONE
        cls.his_attacked_deck = None
        cls.my_attacked_deck = None
        cls.decks_tx_ended = False
        cls.slaveReady = not isMaster

        configs = []
        with open(cls.configfile) as file:
            configs = [line.strip() for line in file]

        if isMaster:
            cls.myName = configs[0]
            cls.hisName = configs[1]
        else:
            cls.myName = configs[1]
            cls.hisName = configs[0]

        if cls.began:
            return

        cls.channel_name = cls.channel_name + configs[0]

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = configs[2]
        pnconfig.publish_key = configs[3]
        pnconfig.user_id = cls.myName
        cls.pubnub = PubNub(pnconfig)
        cls.pubnub.add_listener(MySubscribeCallback())
        cls.pubnub.subscribe().channels(cls.channel_name).execute()
        cls.began = True

    @classmethod
    def send(cls, str):
        SB_link.pubnub.publish().channel(SB_link.channel_name).\
            message(SB_link.myName + ':' + str).sync()
        # pn_async(sb_link.my_publish_callback)

    decks_recieved = []
    isHeLose = False
    isILose = False
    attack_result = SB_attack_result.NONE
    his_attacked_deck = None
    my_attacked_deck = None
    decks_tx_ended = False

    @classmethod
    def read(cls, str):
        data = str.split(':')
        if not data[0] == SB_link.hisName:
            return
        SB_link.parse(data[1])

    @classmethod
    def attack(cls, x, y):
        if not cls._DBGWAITFLAG:
            cls._DBGWAITFLAG = True
        SB_link.his_attacked_deck = SB_pair([x, y])
        SB_link.send(f"h{x},{y}")

    @classmethod
    def result(cls, res):
        SB_link.send(f"r{res}")

    @classmethod
    def sendDecks(cls, decks):
        for d in decks:
            SB_link.send(f"s{d[0]},{d[1]}")
        SB_link.send('q')

    @classmethod
    def sendReadyFlag(cls):
        SB_link.send('Q')

    @classmethod
    def lose(cls):
        SB_link.send('l')

    @classmethod
    def parse(cls, str):
        if str[0] == 'h':
            SB_link.my_attacked_deck = \
                SB_pair([int(x) for x in str[1:].split(sep=",")])
        elif str[0] == 'r':
            SB_link.attack_result = int(str[1])
        elif str[0] == 's':
            SB_link.decks_recieved += \
                [SB_pair([int(x) for x in str[1:].split(sep=",")])]
        elif str[0] == 'l':
            SB_link.isHeLose = True
        elif str[0] == 'q':
            SB_link.decks_tx_ended = True
        elif str[0] == 'Q':
            SB_link.slaveReady = True

    '''@classmethod
    def my_publish_callback(cls, envelope, status):
        # Check whether request successfully completed or not
        ...
        """
        if not status.is_error():
            pass
            #print('   sending: success')
        else:
            print('   sending: fail')
        """
    '''


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        SB_link.read(message.message)


if __name__ == "__main__":
    print("This module is not for direct call!")
