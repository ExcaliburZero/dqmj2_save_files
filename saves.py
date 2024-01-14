from dataclasses import dataclass
from typing import IO, List

import sys

from data_locations import *

ENDIANESS = "little"  # confirmed for DQJ2 save files


@dataclass
class SaveDataRaw:
    raw: List[bytes]

    @property
    def data_checksum(self) -> int:
        return int.from_bytes(
            self.raw[DATA_CHECKSUM_START : DATA_CHECKSUM_END + 1], ENDIANESS
        )

    @property
    def header_checksum(self) -> int:
        return int.from_bytes(
            self.raw[HEADER_CHECKSUM_START : HEADER_CHECKSUM_END + 1], ENDIANESS
        )

    @staticmethod
    def __checksum(data: List[bytes]) -> int:
        num = 0
        i = 0
        j = 0
        while i < DATA_SIZE:
            value = int.from_bytes(data[j * 4 : j * 4 + 4], ENDIANESS)

            num += value
            num = num & 0xFFFFFFFF

            i += 4
            j += 1

        return num

    def calculate_data_checksum(self) -> int:
        return SaveDataRaw.__checksum(self.raw[HEADER_SIZE:])

    def calculate_header_checksum(self) -> int:
        # Assert just in case data checksum is out of date, since it is an input to the header
        # checksum
        assert self.data_checksum == self.calculate_data_checksum()

        return SaveDataRaw.__checksum(self.raw[: DATA_CHECKSUM_END + 1])

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveDataRaw":
        return SaveDataRaw(input_stream.read(HEADER_SIZE + DATA_SIZE))


@dataclass
class Header:
    data_checksum: int
    header_checksum: int


@dataclass
class SaveData:
    header: Header

    @staticmethod
    def from_raw(raw: "SaveDataRaw") -> "SaveData":
        data_checksum = raw.data_checksum
        header_checksum = raw.header_checksum

        print(raw.calculate_data_checksum())
        print(raw.calculate_header_checksum())

        return SaveData(
            Header(
                data_checksum=data_checksum,
                header_checksum=header_checksum,
            )
        )

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveData":
        raw = SaveDataRaw.from_sav(input_stream)

        return SaveData.from_raw(raw)


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as input_stream:
        data = SaveData.from_sav(input_stream)
        print(data)
