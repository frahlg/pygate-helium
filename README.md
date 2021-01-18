For setting up the Pycom Pygate as a package forwarder to the Helium Miner. The device needs to be flashed with the PyGate firmware. The code is the standard code from Pycom with some added features.

In order to get this PyGate to work with the Helium network you need to set up a miner software, the tutorial is described here. You need to set this up on a server or a Raspberry Pi. There is not a requirement to open up ports in the firewall, it works anyway.

https://developer.helium.com/blockchain/run-your-own-miner

The config file is not the standard config provided with the basic PyGate example from Pycom, but instead this one is used https://github.com/Lora-net/packet_forwarder/blob/master/lora_pkt_fwd/global_conf.json

NOTE. You need to change the internal address to the miner.

Changes from the basic Pycom Pygate example:

https://development.pycom.io/tutorials/all/pygate/
https://docs.pycom.io/firmwareapi/pycom/machine/pygate/

- Added both Ethernet and WiFi connection
- It first tries to get an Ethernet connection via DHCP, if not successful it proceeds to WiFi.
- A function (threaded) that periodically checks for connectivity, if disconnected it connects again.

