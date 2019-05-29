## Local

Python: Python 3.6.1

Run:

    $ python server.py
    [2019-05-29 15:45:01] starting up on 0.0.0.0 port 10000
    [2019-05-29 15:45:01] waiting for a connection
    [2019-05-29 15:45:34] waiting for a connection
    [2019-05-29 15:45:34] connection from ('192.168.1.35', 54934)
    [2019-05-29 15:45:34] received "b'ping 0'"
    [2019-05-29 15:45:34] sending data back to the client


## Device

Board: https://adafruit.com/product/4000

https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI at commit ac4aee5d8a2ed5ba4bb2371ab97292376c95021d

Device layout at the time of testing:

    /Volumes/CIRCUITPY/
    ├── code.py
    ├── lib
    │   ├── adafruit_bus_device
    │   │   ├── __init__.py
    │   │   ├── i2c_device.mpy
    │   │   └── spi_device.mpy
    │   ├── adafruit_esp32spi
    │   │   ├── adafruit_esp32spi.py
    │   │   ├── adafruit_esp32spi_requests.py
    │   │   ├── adafruit_esp32spi_socket.py
    │   │   └── adafruit_esp32spi_wifimanager.py
    │   ├── neopixel.mpy
    │   └── simpleio.mpy
    ├── secrets.py

Output:

    Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
    code.py output:
    start with firmware bytearray(b'1.3.0\x00')
    [init] connect!
    [mainloop] try to ping
    [mainloop] > b'ping 0'
    < b'ping 0'
    [mainloop] try to ping
    [mainloop] > b'ping 1'
    < b'ping 1'
    [mainloop] try to ping
    [mainloop] > b'ping 2'
    [mainloop] try to ping
    [mainloop] > b'ping 3'
    < b'ping 2ping 3'
    [mainloop] try to ping
    [mainloop] > b'ping 4'
    [mainloop] try to ping
    [mainloop] > b'ping 5'
    < b'ping 4ping 5'
