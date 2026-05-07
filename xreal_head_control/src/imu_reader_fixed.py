# Fixed IMU Reader for XREAL One Pro
# Uses header-to-header message framing (134-byte messages)
# Adapted from Daniel Sami Mitwalli's original by Het Patel

import socket
import struct
import time
import math
import logging
from typing import Optional, Callable
from src.imu_data import IMUData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IP = "169.254.2.1"
PORT = 52998
TIMEOUT = 5

HEADER = bytes.fromhex("283600000080")
SENSOR_MSG = bytes.fromhex("00401f000040")
RAD_TO_DEG = 180.0 / math.pi

# IMU data starts at offset 26 (header:6 + session:8 + invariant:2 + static:10)
IMU_START = 26


class IMUReaderFixed:
    def __init__(self, ip: str = IP, port: int = PORT, timeout: int = TIMEOUT,
                 callback: Optional[Callable[[IMUData, int, float], None]] = None):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None
        self.message_count = 0
        self.start_time: Optional[float] = None
        self.callback = callback or self.default_callback
        self.logger = logging.getLogger(__name__)

    def default_callback(self, imu_data: IMUData, message_count: int, rate: float) -> None:
        print(f"[{message_count:06d}] {rate:.1f}Hz | {imu_data}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        if self.start_time:
            elapsed = time.time() - self.start_time
            avg_rate = self.message_count / elapsed if elapsed > 0 else 0
            self.logger.info(f"Processed {self.message_count} messages in {elapsed:.1f}s (avg {avg_rate:.1f}Hz)")

    def decode_imu_from_message(self, msg: bytes) -> Optional[IMUData]:
        """Extract IMU data from a 134-byte message using header-to-header framing."""
        sensor_pos = msg.find(SENSOR_MSG)
        if sensor_pos < 0:
            return None

        imu_section = msg[IMU_START:sensor_pos]
        if len(imu_section) < 24:
            return None

        # Skip first 8 bytes (flags/counter), then 6 floats
        data_offset = 8 if len(imu_section) >= 32 else 0
        float_data = imu_section[data_offset:data_offset + 24]
        if len(float_data) < 24:
            return None

        try:
            values = [struct.unpack('<f', float_data[i:i+4])[0] for i in range(0, 24, 4)]
            return IMUData(
                gx=values[0] * RAD_TO_DEG, gy=values[1] * RAD_TO_DEG, gz=values[2] * RAD_TO_DEG,
                ax=values[5], ay=values[4], az=values[3]
            )
        except (ValueError, struct.error):
            return None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.logger.info(f"Connecting to {self.ip}:{self.port}...")
        self.sock.connect((self.ip, self.port))
        self.logger.info("TCP connected!")
        self.start_time = time.time()

    def run(self):
        recv_buffer = b""
        try:
            if not self.sock:
                self.connect()

            while True:
                try:
                    data = self.sock.recv(4096)
                    if not data:
                        self.logger.info("Connection closed by device.")
                        break

                    recv_buffer += data

                    # Split on HEADER to get complete messages
                    while True:
                        h1 = recv_buffer.find(HEADER)
                        if h1 == -1:
                            break
                        h2 = recv_buffer.find(HEADER, h1 + len(HEADER))
                        if h2 == -1:
                            break

                        msg = recv_buffer[h1:h2]
                        recv_buffer = recv_buffer[h2:]

                        imu_data = self.decode_imu_from_message(msg)
                        if imu_data:
                            self.message_count += 1
                            elapsed = time.time() - self.start_time
                            rate = self.message_count / elapsed if elapsed > 0 else 0
                            self.callback(imu_data, self.message_count, rate)

                except socket.timeout:
                    self.logger.warning("Socket timeout - retrying...")
                    continue
                except KeyboardInterrupt:
                    self.logger.info("Stopping...")
                    break

        except ConnectionRefusedError:
            self.logger.error(f"Connection refused. Is the device at {self.ip}:{self.port} available?")
        except Exception as e:
            self.logger.error(f"Error: {e}")
        finally:
            self.disconnect()
