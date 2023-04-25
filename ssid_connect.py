import socketpool
import wifi
import os

print("Connecting to WiFi")

for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")

ssid = os.getenv('CIRCUITPY_WIFI_SSID')
passwd = os.getenv('CIRCUITPY_WIFI_PASSWORD')
wifi.radio.connect(ssid, passwd)

ip = wifi.radio.ipv4_address
print(f"Connected: {ip}")

pool = socketpool.SocketPool(wifi.radio)
