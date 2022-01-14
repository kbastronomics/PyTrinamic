from serial import Serial, SerialException
import serial.tools.list_ports;
from PyTrinamic.connections.tmcl_interface import tmcl_interface


class serial_tmcl_interface(tmcl_interface):
    """
    Opens a serial TMCL connection
    """
    def __init__(self, com_port, datarate=115200, host_id=2, module_id=1, debug=False):
        if type(comPort) != str:
            raise TypeError;

        super().__init__(host_id, module_id, debug)

        self._baudrate = datarate

        try:
            self._serial = Serial(com_port, self._baudrate)
        except SerialException as e:
            raise ConnectionError from e

        self._serial.timeout = 5

        if self._debug:
            print("Open port: " + self._serial.portstr)

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        """
        Close the connection at the end of a with-statement block.
        """
        del exit_type, value, traceback
        self.close()

    def close(self):
        if self._debug:
            print("Close port: " + self._serial.portstr)

        self._serial.close()
        return 0;

    def _send(self, host_id, module_id, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id

        self._serial.write(data)

    def _recv(self, host_id, module_id):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id

        data = self._serial.read(9)

        if len(data) != 9:
            raise RuntimeError("TMCL datagram timed out")

        return data

    def set_timeout(self, timeout):
        self._serial.timeout = timeout if timeout != 0 else None

    def get_timeout(self):
        return self._serial.timeout

    def printInfo(self):
        print("Connection: type=serial_tmcl_interface com=" + self._serial.portstr + " baud=" + str(self._baudrate))

    def enableDebug(self, enable):
        self._debug = enable

    @staticmethod
    def supportsTMCL():
        return True

    @staticmethod
    def supportsCANopen():
        return False

    @staticmethod
    def list():
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        connected = []
        for element in sorted(serial.tools.list_ports.comports()):
            connected.append(element.device)

        return connected
