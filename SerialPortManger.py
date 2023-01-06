import serial


class SerialPortManager:
    def __init__(self, com_port, baud_rate, timeout):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.__initialization_handshake__()

    def __initialization_handshake__(self):
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=self.timeout)
        read_line = self.serial_port.readline().decode().strip()
        assert read_line == "Device is ready ...", f"What is {read_line}"
        self.serial_port.write('0'.encode())
        read_line = self.serial_port.readline().decode().strip()
        assert read_line == "Operational Mode"

    def restart(self):
        del self.serial_port
        self.__initialization_handshake__()

    def read_delay(self):
        try:
            arduino_delay = int(self.serial_port.readline().decode().strip().split(' ')[-1]) // 1000
        except:
            arduino_delay = None

        return arduino_delay

