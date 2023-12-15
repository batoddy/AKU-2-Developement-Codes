import serial.tools.list_ports
import serial

port_list = list(serial.tools.list_ports.comports())

for port, desc, hwid in sorted(port_list):
        print("{}".format(port))

