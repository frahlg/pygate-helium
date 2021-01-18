from network import WLAN
from network import ETH
import time
import machine
from machine import RTC
import pycom
import _thread

print('\nStarting LoRaWAN concentrator')
# Disable Hearbeat
pycom.heartbeat(False)

# Define callback function for Pygate events
def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        pycom.rgbled(0x103300)
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        pycom.rgbled(0x331000)
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        pycom.rgbled(0x000000)

# register callback function
machine.callback(trigger = (machine.PYGATE_START_EVT | machine.PYGATE_STOP_EVT | machine.PYGATE_ERROR_EVT), handler=machine_cb)

def connect_network():
    global net
    print('Connecting over Ethernet...')
    net = ETH()
    net.init(hostname='pygate')
    timer_counter = 0
    while not net.isconnected():
        print('.',end='')
        time.sleep(1)
        timer_counter += 1
        if timer_counter > 10: break

    if net.isconnected():
        print(net.ifconfig())
        print('OK Ethernet connected ...')
    else:
        print('Ethernet not connected, trying WiFi...')
        print('Connecting to WiFi...',  end='')
        # Connect to a Wifi Network
        net = WLAN(mode=WLAN.STA)
        net.connect(ssid='YOUR SSID HERE', auth=(WLAN.WPA2, 'YOUR PASSWORD HERE'))
        timer_counter = 0
        while not net.isconnected():
            print('.', end='')
            time.sleep(1)
            timer_counter += 1
            if timer_counter == 60:
                print('WiFi failed to connect')
                break
        if net.isconnected(): print("OK WiFi connected ... ")

connect_network()

def check_network_up():
    global net
    while True:
        if not net.isconnected():
            connect_network()
        else:
            print('Network check')
        time.sleep(30)

_thread.start_new_thread(check_network_up, ())

# Sync time via NTP server for GW timestamps on Events
print('Syncing RTC via ntp...', end='')
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    print('.', end='')
    time.sleep(.5)
print(" OK\n")

# Read the GW config file from Filesystem
fp = open('/flash/config.json','r')
buf = fp.read()

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)
