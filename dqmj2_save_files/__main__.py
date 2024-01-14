from typing import List

import click

from . import saves


@click.command()
@click.argument("save_filepath")
def describe(save_filepath: str) -> int:
    with open(save_filepath, "rb") as input_stream:
        data = saves.SaveData.from_sav(input_stream)
        print(data)


if __name__ == "__main__":
    describe()
