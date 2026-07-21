"""The core sondbus implementation."""

import struct

from crc import Calculator, Crc8
import serial

SYNC_SEQUENCE: bytes = bytes(
    [
        0x1F,
        0x2E,
        0x3D,
        0x4C,
        0x5B,
        0x6A,
        0x79,
        0x88,
        0x97,
        0xA6,
        0xB5,
        0xC4,
        0xD3,
        0xE2,
        0xF1,
    ]
)
START_BYTE: int = 0x55
CMD_SYNC: int = 0x01


def calc_crc(data: bytes | bytearray) -> int:
    calculator = Calculator(Crc8.AUTOSAR)
    return calculator.checksum(data)


class CRCError(Exception):
    pass


class Master:
    def __init__(self, port: serial.Serial):
        self.port = port
        self.sync_sequence = 0

    def make_cmd(self, cmd: int) -> int:
        sync = self.sync_sequence
        self.sync_sequence += 1

        return cmd | (sync & 0b11) << 6

    def sync(self):
        data = bytearray()
        data.append(self.make_cmd(CMD_SYNC))
        data.extend(SYNC_SEQUENCE)
        data.append(1)
        data.append(calc_crc(data))

        self.port.write(data)

    def read_broadcast(self, offset: int, length: int) -> bytes:
        length = length & 0xFF
        offset = offset & 0xFF

        cmd_byte = 0 | 1 << 5 

        data = bytearray()
        data.append(self.make_cmd(cmd_byte))
        data.extend(struct.pack(">B", offset))
        data.extend(struct.pack(">B", length))
        data.append(calc_crc(data))

        self.port.write(data)

        rx = self.port.read(length + 1)

        payload = rx[:-1]
        data.extend(payload)

        calced_crc = calc_crc(data)
        crc = rx[length]

        if crc != calced_crc:
            raise CRCError

        return payload
