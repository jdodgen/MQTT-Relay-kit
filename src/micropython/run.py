# simple relay controler
# built from mqtt_as event demo
# modifications Jim Dodgen 2023
# MIT Licence

from mqtt_as import MQTTClient, config
import relay_config
from relay import relay
import uasyncio as asyncio
import time
import ntptime


# Local configuration
config['ssid'] = relay_config.ssid  # Optional on ESP8266
config['wifi_pw'] = relay_config.passwd
config['server'] = relay_config.server  # Change to suit e.g. 'iot.eclipse.org'

r = relay(relay_config.relay_pin)
def stat_msg():
    t = time.localtime()
    time_string = str(t[0])+"-"+str(t[1])+"-"+str(t[2])+"-"+str(t[3])+"-"+str(t[4])
    print(time_string)
    return bytes(r.current_state()+"/"+time_string, 'utf-8')

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        top = topic.decode('utf-8')
        cmd = msg.decode('utf-8')
        print(top, cmd, retained)
        if (cmd == "on"):
            r.turn_on()
        else:
            r.turn_off()
        
        await client.publish(relay_config.pub_topic, stat_msg(), qos = 1, retain=True)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        print("subscribing")
        await client.subscribe(relay_config.sub_topic, 1)  # renew subscriptions

async def main(client):
    while True:
        print("checking connection")
        try:
            await client.connect()
        except:
            pass
        else:
            break
    ntptime.settime()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    await asyncio.sleep(5)
    #stat_msg = bytes(r.current_state()+"/"+str(time.time()), 'utf-8')
    await client.publish(relay_config.pub_topic, stat_msg(), qos = 1, retain=True)
    while True:
        await asyncio.sleep(60)
        print('publish current state', r.current_state())
        # If WiFi is down the following will pause for the duration.
        #await client.publish('result', '{}'.format(n), qos = 1)
        #await client.publish(relay_config.pub_topic, bytes(str(n), 'utf-8'), qos = 1)
        #stat_msg = bytes(r.current_state()+"/"+str(time.time()), 'utf-8')
        await client.publish(relay_config.pub_topic, stat_msg(), qos = 1, retain=True)
       

print("starting")

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
print("example exiting")