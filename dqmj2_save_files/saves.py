from dataclasses import dataclass
from typing import IO, List

import datetime

from . import character_set
from .data_locations import *

ENDIANESS = "little"  # confirmed for DQJ2 save files


@dataclass
class SaveDataRaw:
    raw: bytearray

    @property
    def data_checksum(self) -> int:
        return int.from_bytes(
            self.raw[DATA_CHECKSUM_START : DATA_CHECKSUM_END + 1], ENDIANESS
        )

    @data_checksum.setter
    def data_checksum(self, checksum: int) -> int:
        checksum_bytes = checksum.to_bytes(4, ENDIANESS)
        for i, b in enumerate(checksum_bytes):
            self.raw[i + DATA_CHECKSUM_START] = b

    @property
    def header_checksum(self) -> int:
        return int.from_bytes(
            self.raw[HEADER_CHECKSUM_START : HEADER_CHECKSUM_END + 1], ENDIANESS
        )

    @header_checksum.setter
    def header_checksum(self, checksum: int) -> int:
        checksum_bytes = checksum.to_bytes(4, ENDIANESS)
        for i, b in enumerate(checksum_bytes):
            self.raw[i + HEADER_CHECKSUM_START] = b

    @property
    def play_time(self) -> datetime.timedelta:
        play_time_frames = int.from_bytes(
            self.raw[PLAY_TIME_START : PLAY_TIME_END + 1], ENDIANESS
        )

        return datetime.timedelta(seconds=play_time_frames) / 30

    @property
    def player_name(self) -> str:
        characters = [
            SaveDataRaw.__int_to_char(i)
            for i in self.raw[PLAYER_NAME_START : PLAYER_NAME_END + 1]
        ]

        return "".join(characters)

    @property
    def gold(self) -> int:
        return int.from_bytes(self.raw[GOLD_START : GOLD_END + 1], ENDIANESS)

    @property
    def atm(self) -> int:
        return int.from_bytes(self.raw[ATM_START : ATM_END + 1], ENDIANESS)

    @property
    def victories(self) -> int:
        return int.from_bytes(self.raw[VICTORIES_START : VICTORIES_END + 1], ENDIANESS)

    @staticmethod
    def __int_to_char(i: int) -> str:
        if i == 0:
            return ""

        return character_set.int_to_char(i)

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

    def calculate_header_checksum(
        self, allow_invalid_data_checksum: bool = False
    ) -> int:
        # Assert just in case data checksum is out of date, since it is an input to the header
        # checksum
        assert allow_invalid_data_checksum or (
            self.data_checksum == self.calculate_data_checksum()
        )

        return SaveDataRaw.__checksum(self.raw[: DATA_CHECKSUM_END + 1])

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveDataRaw":
        return SaveDataRaw(bytearray(input_stream.read(HEADER_SIZE + DATA_SIZE)))

    def write_sav(self, output_stream: IO[bytes]) -> None:
        output_stream.write(self.raw)


@dataclass
class Header:
    data_checksum: int
    header_checksum: int


@dataclass
class Data:
    play_time: datetime.timedelta
    player_name: str
    gold: int
    atm: int
    victories: int


@dataclass
class SaveData:
    header: Header
    data: Data

    @staticmethod
    def from_raw(raw: "SaveDataRaw") -> "SaveData":
        data_checksum = raw.data_checksum
        header_checksum = raw.header_checksum

        play_time = raw.play_time
        player_name = raw.player_name
        gold = raw.gold
        atm = raw.atm
        victories = raw.victories

        return SaveData(
            Header(
                data_checksum=data_checksum,
                header_checksum=header_checksum,
            ),
            Data(
                play_time=play_time,
                player_name=player_name,
                gold=gold,
                atm=atm,
                victories=victories,
            ),
        )

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveData":
        raw = SaveDataRaw.from_sav(input_stream)

        return SaveData.from_raw(raw)
