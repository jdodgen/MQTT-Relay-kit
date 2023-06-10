import os
# this configures and installs router software
# change relay_config_template to your system/network
# the {}'s are replaced with MQTT Topic name
relay_config_template = """
ssid = 'JEDguest' 
passwd = '9098673852'
server = 'home-broker.local'
sub_topic = "{}"
pub_topic = "{}_status"
relay_pin = 35
"""
print("each relay must have a unique topic name")
print("input topic")
topic=input()

cooked_cfg = relay_config_template.format(topic,topic)
with open('relay_config.py', 'w') as f:
    f.write(cooked_cfg)

print("install micropython? (Y,n)")
ans = input()
if (ans.upper() != "N"):
    os.system("esptool.py --port /dev/ttyACM0 erase_flash")
    os.system("esptool.py --chip esp32s2 --port /dev/ttyACM0 write_flash -z 0x1000 GENERIC_S2-20230426-v1.20.0.bin")

code = [
"run.py",
"main.py",
"relay.py",
"mqtt_as.py",
"boot.py",
"relay_config.py",
]

print("now pushing python code")
for c in code:
    print("installing", c)
    os.system("ampy --port /dev/ttyACM0 put "+c)

os.system("ampy --port /dev/ttyACM0 ls")