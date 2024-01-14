from typing import List

import click

from . import saves


@click.command()
@click.argument("save_filepath")
def describe(save_filepath: str) -> int:
    with open(save_filepath, "rb") as input_stream:
        data = saves.SaveData.from_sav(input_stream)

    print_header(data.header)
    print_data(data.data)


def print_header(header: saves.Header) -> None:
    fields = [
        ("Data checksum", header.data_checksum),
        ("Header checksum", header.header_checksum),
    ]

    print("Header:")
    for name, value in fields:
        print(f"\t{name}: {value}")


def print_data(data: saves.Data) -> None:
    fields = [
        ("Play time", data.play_time),
        ("Player name", data.player_name),
        ("Gold", data.gold),
    ]

    print("Data:")
    for name, value in fields:
        print(f"\t{name}: {value}")


if __name__ == "__main__":
    describe()
