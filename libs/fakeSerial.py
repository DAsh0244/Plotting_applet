# fakeSerial.py
# A very crude simulator for PySerial assuming it
# is emulating a generic device.
# a Serial class emulator

from os import urandom
RX_BUF = urandom(1024*10)

class SerialBase:
    # create control bytes
    XON = bytes([17])
    XOFF = bytes([19])

    CR = bytes([13])
    LF = bytes([10])
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
                 9600, 19200, 38400, 57600, 115200)
    PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
    STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
    FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
    BYTESIZES = (FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)
    PARITIES = (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE)
    STOPBITS = (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

    def __init__(self, port='COM1', baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None,
                 dsrdtr=False, inter_byte_timeout=None, **kwargs):
        """
        Initialize comm port object. If a "port" is given, then the port will be
        opened immediately. Otherwise a Serial port object in closed state
        is returned.
        """
        self.is_open = False
        self.portstr = None
        self.name = None
        # correct values are assigned below through properties
        self._port = None
        self._baudrate = None
        self._bytesize = None
        self._parity = None
        self._stopbits = None
        self._timeout = None
        self._write_timeout = None
        self._xonxoff = None
        self._rtscts = None
        self._dsrdtr = None
        self._inter_byte_timeout = None
        self._rs485_mode = None  # disabled by default
        self._rts_state = True
        self._dtr_state = True
        self._break_state = False
        # assign values using get/set methods using the properties feature
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        # watch for backward compatible kwargs
        if 'writeTimeout' in kwargs:
            self.write_timeout = kwargs.pop('writeTimeout')
        if 'interCharTimeout' in kwargs:
            self.inter_byte_timeout = kwargs.pop('interCharTimeout')
        if kwargs:
            raise ValueError('unexpected keyword arguments: {!r}'.format(kwargs))

        if port is not None:
            self.open()

    def isOpen(self):
        """
        Returns True if the port is open. False otherwise
        """
        return self._isOpen

    def open(self):
        """
        sets port to be open
        """
        self._isOpen = True

    def close(self):
        """
        sets port to be closed
        """
        self._isOpen = False


class serialutil():
    class SerialException(IOError):
        """Base class for serial port related exceptions."""


class tools:

    class list_ports:

        @staticmethod
        def comports():
            from random import randrange
            ports = []
            for i in range(0, randrange(7)):  # 0 - 6 possible
                if i != 0:
                    ports.append('COM{}'.format(i))
            return ports

def ser_id_gen(n):
    from os import urandom
    from binascii import b2a_hex
    return b2a_hex(urandom(n))

class Serial(SerialBase):
    def __init__(self, **kwargs):
        super(Serial, self).__init__(**kwargs)
        self._TX_buf = ''
        self._RX_buf = RX_BUF
        self._id = ser_id_gen(3)

    def write(self, string):
        """
        writes a string of characters to the fake device
        """
        print('Device sent : "' + string + '"')
        self._TX_buf += string

    def read(self, n=1):
        """
        reads n characters from the fake device.
        """
        s = self._RX_buf[0:n]
        self._RX_buf = self._RX_buf[n:]
        # print("read op occurred: RX_buf = {}".format(self._RX_buf), end='\n\n')
        return s  # bytes(s, encoding='ascii')

    def readline(self):
        """
        reads characters from the fake device until a \n is found.
        """
        returnIndex = self._RX_buf.index("\n")  # \r\n technically
        if returnIndex != -1:
            s = self._RX_buf[0:returnIndex + 1]
            self._RX_buf = self._RX_buf[returnIndex + 1:]
            return s  # bytes(s, encoding='ascii')  # s
        else:
            return 0x04  # ''

    def __str__(self):
        """
        returns a string representation of the serial class
        """
        # noinspection PyUnresolvedReferences
        return 'Serial <id=0x{}, open={}> ( port="{}", baudrate={}, bytesize={}, parity="{}", stopbits={}, ' \
               'xonxoff={}, rtscts={})'.format(str(self._id, 'utf-8'), str(self.isOpen()), self.port, self.baudrate,
                                               self.bytesize, self.parity, self.stopbits, self.xonxoff, self.rtscts)

if __name__ == '__main__':
    import sys
    from math import ceil
    ser = Serial(port='COM22', baudrate=19200, stopbits=Serial.STOPBITS_TWO, xonxoff=True)
    for i in range(0, ceil(len(RX_BUF)/8)):
        print('{}:{}'.format(i, ser.read(8)))
    sys.exit(0)
