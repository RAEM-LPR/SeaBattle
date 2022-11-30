from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from sb_helpers import sb_pair


"""
Протокол
    name:cmd
Комманды:
    hx,y - выстрел по x,y
    rn - результат выстрела; n: 0 - мимо, 1 - попал, 2 - убил
    l - lose
    sx,y - палуба на x,y
# x,y,n - числа
"""


class sb_link:
    channel_name = "seabattle"  # 'my_channel'
    pubnub = None
    configfile = "keys.txt"
    """
    1 строка - имя игрока, ходящего первым
    2 строка - имя игрока, ходящего вторым
    3 строка - PubNub subscribe_key
    4 строка - PubNub publish_key
    """
    myName = ''
    hisName = ''

    @classmethod
    def begin(cls, isMaster):
        configs = []
        with open(sb_link.configfile) as file:
            configs = [line for line in file]

        if isMaster:
            sb_link.myName = configs[0]
            sb_link.hisName = configs[1]
        else:
            sb_link.myName = configs[1]
            sb_link.hisName = configs[0]

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = configs[2]
        pnconfig.publish_key = configs[3]
        pnconfig.user_id = sb_link.myName
        sb_link.pubnub = PubNub(pnconfig)
        sb_link.pubnub.add_listener(MySubscribeCallback())
        sb_link.pubnub.subscribe().channels(sb_link.channel_name).execute()

    @classmethod
    def my_publish_callback(cls, envelope, status):
        # Check whether request successfully completed or not
        """
        if not status.is_error():
            pass
            #print('   sending: success')
        else:
            print('   sending: fail')
        """

    @classmethod
    def send(cls, str):
        print(sb_link.myName + ':' + str) #FIXME DEBUG
        #sb_link.pubnub.publish().channel(sb_link.channel_name).message(sb_link.myName + ':' + str).pn_async(sb_link.my_publish_callback)
    """
    Протокол
        name:cmd
    Комманды:
        hx,y - выстрел по x,y
        rn - результат выстрела; n: 0 - мимо, 1 - попал, 2 - убил
        l - lose
        sx,y - палуба на x,y
    # x,y,n - числа
    """
    # не отправляем новый запрос, пока не обработали старый
    # s** копим в массиве
    ldecks = None 
    lheLose = False
    lresult = -2
    lattack = None
    lshoot = None
    available = False

    @classmethod
    def read(cls, str):
        data = str.split(':')
        if not data[0] == sb_link.hisName:
            return
        sb_link.parse(data[1]) 

    @classmethod
    def attack(cls, x, y):
        sb_link.ldecks=sb_pair([x,y])
        sb_link.send(f"h{x},{y}") 

    @classmethod
    def result(cls, res):
        sb_link.send(f"h{res}") 

    @classmethod
    def parse(cls, str):
        sb_link.available = True
        if str[0] == 'h':
            sb_link.lattack = sb_pair([int(x) for x in str.split("h,")])
        elif str[0] == 'r':
            sb_link.result=int(str[1])
        elif str[0] == 's':
            sb_link.ldecks = sb_pair([int(x) for x in str.split("h,")])
        elif str[0] == 'l':
            sb_link.lheLose = True  
        else:
            sb_link.available = False   

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            ... # pubnub.publish().channel('my_channel').message('Hello world!').pn_async(sb_link.my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        sb_link.read(message.message)  # print(message.message)

if __name__ == "__main__":
    print("This module is not for direct call!")
