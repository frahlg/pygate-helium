The device needs to be flashed with the PyGate firmware. The code is the standard code from Pycom with some added features.

In order to get this PyGate to work with the Helium network you need to set up a miner software, https://developer.helium.com/blockchain/run-your-own-miner
The config file, https://github.com/Lora-net/packet_forwarder/blob/master/lora_pkt_fwd/global_conf.json

- Added both Ethernet and WiFi connection
- It first tries to get an Ethernet connection via DHCP, if not successful it proceeds to WiFi.
- A function (threaded) that periodically checks for connectivity, if disconnected it connects again.