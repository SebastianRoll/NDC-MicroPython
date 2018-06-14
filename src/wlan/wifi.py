import network

known_wlan = {
    b'kubernetes lifeline': b"workwork",
    b'HackheimWifi': b'TeletextFTW',
}

wlan = network.WLAN(network.STA_IF)
if not wlan.active() or not wlan.isconnected():
    wlan.active(True)
    for (ssid, bssid, channel, RSSI, authmode, hidden) in wlan.scan():
        print(ssid)
        pwd = known_wlan.get(ssid)
        if pwd:
            print("Found {}".format(ssid))
            wlan.connect(ssid, pwd)
            while not wlan.isconnected():
                pass
        # if wlan.isconnected():
        #     print("Connected to {}".format(ssid))
        #     print(wlan.ifconfig())
            # break
