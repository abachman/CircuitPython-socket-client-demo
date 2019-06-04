# pylint: disable=unused-import, import-error, missing-docstring
# pylint: disable=attribute-defined-outside-init, invalid-name, protected-access

import time

from secrets import secrets

import board
import busio
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

# pixel ring
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# Initialize WiFi Module
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset, debug=False)
print("start with firmware", esp.firmware_version)

dot.fill((255, 0, 0))

class SocketClient:
    def __init__(self, _secrets):
        # set global network interface for the socket library
        self.secrets = _secrets

        self.host = esp.unpretty_ip(self.secrets['host'])
        self.port = self.secrets['port']

        self.esp = None
        self.sock = None

    def reset(self):
        self.esp.reset()
        self.sock = None

    def set_interface(self, _esp):
        self.esp = _esp
        socket.set_interface(_esp)

    def connect(self):
        while not self.wifi_connected:
            try:
                self.esp.connect_AP(
                    bytes(self.secrets['ssid'], 'utf-8'),
                    bytes(self.secrets['password'], 'utf-8')
                )
            except RuntimeError:
                time.sleep(1)

        if not self.socket_connected:
            self.reconnect_socket()

    @property
    def wifi_connected(self):
        return self.esp.is_connected

    @property
    def socket_connected(self):
        return self.wifi_connected and self.sock and self.esp.socket_connected(self.sock._socknum)

    def reconnect_socket(self):
        self.message_count = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            self.sock.connect((self.host, self.port), esp.TCP_MODE)
        except RuntimeError as ex:
            print("[SocketClient reconnect] err", ex, "sleep and retry")
            time.sleep(1)
            self.reconnect_socket()

    def write(self, _bytes):
        self.sock.write(_bytes)
        self.message_count += 1

    def read(self):
        return self.sock.read()

client = SocketClient(secrets)
client.set_interface(esp)

while not client.socket_connected:
    try:
        print("[init] connect!")
        client.connect()
    except RuntimeError:
        client.reset()
        time.sleep(1)

while True:
    dot.fill((100, 100, 0))

    if client.socket_connected:
        print("[mainloop] try to ping")
        try:
            to_send = b"ping %i" % client.message_count
            print("[mainloop] >", to_send)
            client.write(to_send)
            time.sleep(0.1)
            data = client.read()
            while data:
                print("<", data)
                data = client.read()
        except RuntimeError as ex:
            # failed to write, maybe the connection went away?
            print("[RuntimeError] error writing to socket.", ex)
            client.connect()
            continue # back to the top
    else:
        print("[mainloop] socket not connected, reconnect")
        try:
            client.connect()
        except RuntimeError:
            print("[mainloop] failed reconnect, reset connection")
            client.reset()
            time.sleep(1)

    dot.fill((0, 0, 255))

    time.sleep(2)
