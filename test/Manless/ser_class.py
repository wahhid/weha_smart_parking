import serial
import time
import threading
import collections

SERIAL_LOG_INFO = 0x01
SERIAL_LOG_NOTICE = 0x02
SERIAL_LOG_WARNING = 0x04
SERIAL_LOG_ERR = 0x05
SERIAL_LOG_DEBUG = 0x6

class Ser:
    """serial class,use thire library: pyserial"""
    def __init__(self):
        # default serial args
        self.serial = serial.Serial()
        self.serial.timeout  = 0.1
        self.serial.port     = "COM1"
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.parity   = "N"
        self.serial.stopbits = 1
        self.max_recv_buf_len = 255

        self._out_packet = collections.deque()
        # serial receive threading
        self._thread = None
        self._thread_terminate = False
        self.serial_alive = False

        self._on_message = None
        self._on_send = None
        self._on_log = None
        self._logger = None
        # callback mutex RLock
        self._callback_mutex = threading.RLock()
        self._open_mutex = threading.Lock()

    def loop_start(self):
        print("Loop Start")
        self._thread = threading.Thread(target=self.loop_forever)
        self._thread.setDaemon(True)
        self._thread.start()

    def loop_forever(self):
        run = True
        while run:
            if self.serial_alive:
                break
            else:
                with self._open_mutex:
                    self._open_serial()
            time.sleep(1)
        while self.serial_alive:
            time.sleep(0.1)
            while run:
                try:
                    b = self.serial.read(self.max_recv_buf_len)
                    if not b:
                        break
                    self._handle_on_message(b)
                    self._easy_log(SERIAL_LOG_INFO, "serial receive message:%s", b)
                except Exception as e:
                    pass

    def _open_serial(self):
        """try to open the serial"""
        if self.serial.port and self.serial.baudrate:
            try:
                if self.serial.isOpen():
                    self._close_serial()
                self.serial.open()
            except serial.SerialException as e:
                # print("[ERR] open serial error!!! %s" % e)
                # self._easy_log(SERIAL_LOG_ERR, "open serial error!!! %s", e)
                raise
            else:
                self.serial_alive = True
                self._thread = threading.Thread(target=self._recv)
                self._thread.setDaemon(True)
                self._thread.start()
                # print("[INFO] open serial success: %s / %s"%(self.serial.port, self.serial.baudrate))
                self._easy_log(SERIAL_LOG_INFO, "open serial success: %s / %s",self.serial.port, self.serial.baudrate)
        else:
            print("[ERR] port is not setting!!!")
            self._easy_log(SERIAL_LOG_ERR, "port is not setting!!!")

    def _close_serial(self):
        try:
            self.serial.close()
            self.serial_alive = False
            self._thread_terminate = False
        except:
            pass

    def _recv(self):
        """serial recv thread"""
        while self.serial_alive:
            time.sleep(0.1)
            while self.serial_alive:
                try:
                    b = self.serial.read(self.max_recv_buf_len)
                    if not b:
                        break
                    # s = str(binascii.b2a_hex(b).decode('utf-8')).upper()
                    self._handle_on_message(b)
                    self._easy_log(SERIAL_LOG_INFO, "serial receive message:%s", b)
                except Exception as e:
                    pass
                    # self.serial_alive = False
                    # self._easy_log(SERIAL_LOG_ERR, "serial err:%s", e)

    @property
    def on_message(self):
        """ If implemented, called when the serial has receive message.
        Defined to allow receive.
        """
        return self._on_message

    @on_message.setter
    def on_message(self, func):
        with self._callback_mutex:
            self._on_message = func

    def _handle_on_message(self, message):
        """serial receive message handle"""
        self.on_message(message)

    def on_send(self, msg):
        """send msg,
        msg: type of bytes or str"""
        with self._callback_mutex:
            if msg:
                if isinstance(msg, bytes):
                    self.serial.write(msg)
                if isinstance(msg, str):
                    self.serial.write(msg.encode('utf-8'))
            self._easy_log(SERIAL_LOG_INFO, "serial send message: %s", msg)

    @property
    def on_log(self):
        """If implemented, called when the serial has log information.
        Defined to allow debugging."""
        return self._on_log

    @on_log.setter
    def on_log(self, func):
        """ Define the logging callback implementation.
        Expected signature is:
            log_callback(level, buf)
        level:      gives the severity of the message and will be one of
                    SERIAL_LOG_INFO, SERIAL_LOG_NOTICE, SERIAL_LOG_WARNING,
                    SERIAL_LOG_ERR, and SERIAL_LOG_DEBUG.
        buf:        the message itself
        """
        self._on_log = func

    def _easy_log(self, level, fmt, *args):
        if self.on_log is not None:
            buf = fmt % args
            try:
                if level == SERIAL_LOG_DEBUG:
                    level = "[DEBUG]"
                if level == SERIAL_LOG_ERR:
                    level = "[ERR]"
                if level == SERIAL_LOG_INFO:
                    level = "[INFO]"
                if level == SERIAL_LOG_NOTICE:
                    level = "[NOTICE]"
                if level == SERIAL_LOG_WARNING:
                    level = "[WARNING]"
                self.on_log(level, buf)
            except Exception:
                pass