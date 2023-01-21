from open_gopro import WirelessGoPro

with WirelessGoPro() as gopro:
    print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get"
          " data now!")
