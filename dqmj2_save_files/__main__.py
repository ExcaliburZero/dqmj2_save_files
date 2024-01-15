from typing import List

import click

from . import saves


@click.command()
@click.argument("save_filepath")
def describe(save_filepath: str) -> int:
    with open(save_filepath, "rb") as input_stream:
        raw_data = saves.SaveDataRaw.from_sav(input_stream)
        data = saves.SaveData.from_raw(raw_data)

    print_header(data.header, raw_data)
    print_data(data.data)


def print_header(header: saves.Header, raw_data: saves.SaveDataRaw) -> None:
    data_checksum_valid = raw_data.data_checksum == raw_data.calculate_data_checksum()
    header_checksum_valid = (
        raw_data.header_checksum
        == raw_data.calculate_header_checksum(allow_invalid_data_checksum=True)
    )

    fields = [
        (
            "Data checksum",
            f"{header.data_checksum} ({'ok' if data_checksum_valid else 'invalid'})",
        ),
        (
            "Header checksum",
            f"{header.header_checksum} ({'ok' if header_checksum_valid else 'invalid'})",
        ),
    ]

    print("Header:")
    for name, value in fields:
        print(f"\t{name}: {value}")


def print_data(data: saves.Data) -> None:
    fields = [
        ("Play time", data.play_time),
        ("Player name", data.player_name),
        ("Gold", data.gold),
        ("ATM", data.atm),
    ]

    print("Data:")
    for name, value in fields:
        print(f"\t{name}: {value}")


if __name__ == "__main__":
    describe()
