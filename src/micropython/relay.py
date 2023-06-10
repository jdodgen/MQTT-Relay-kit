import machine

class relay:
    
    def __init__(self, relay_pin):
        self.relay = machine.Pin(relay_pin,machine.Pin.OUT)
        self.relay.off() # default

    def turn_on(self):
        print('turning relay on(1)  current', self.relay.value())
        self.relay.value(1)

    def turn_off(self):
        print('turning relay off(0) current', self.relay.value())
        self.relay.value(0)
        
    def current_state(self):
        now = self.relay.value()
        if now == 1:
           return "on"
        return "off"
