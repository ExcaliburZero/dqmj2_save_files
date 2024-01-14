Info on the save data file format for Dragon Quest Monsters: Joker 2.

Re-reverse engineered from DQM Joker 2 Save Data Editor (created by asa-o, translated into English by Hynckel and jm_plata):

https://web.archive.org/web/20200303213846/http://www.asa-o.net/tools/dqmj2_cheat

https://www.woodus.com/den/games/dqm5ds/save_data_editor.php

## Format
* Binary
* Little endian

### Header [0x0 to 0x8F]
#### Magic [0x0 to 0x2]
Magic bytes that indicate that this is a DQMJ2 save file.

```
SYN
```

#### Data checksum [0x88 to 0x8B]
Checksum of the data portion of the file.

32bit unsigned integer.

```python
def data_checksum(data: list[bytes]) -> int:
    num = 0
    i = 0
    j = 0
    while i < data_size:
        value = int.from_bytes(data[j * 4:j * 4 + 4], "little")

        num += value
        num = num & 0xffffffff

        i += 4
        j += 1

    return num
```

### Header checksum [0x8C to 0x8F]
Checksum of all prior portions of the header (including the data checksum).

32bit unsigned integer.

```python
def header_checksum(header: list[bytes]) -> int:
    num = 0
    i = 0
    j = 0
    while i < header_size - 4:
        value = int.from_bytes(header[j * 4:j * 4 + 4], "little")

        num += value
        num = num & 0xffffffff

        i += 4
        j += 1

    return num
```

### Data [0x90 to 0x___]
#### Play time [0x90 to 0x94]
Number of frames that the game has been played for. Divide by 30 to get the number of seconds of playtime (30fps?).

32bit unsigned integer. (double check this? might be 64bit)

#### Player name [0x98 to 0x9F]
Name of the player character.

8 characters max. Each character is 1byte in a non-ascii encoding. `0x00` indicates unused character.

#### Gold [0xAC to 0xAF]
Amount of gold the player currently has.

Likely 32bit unsigned integer, but max allowed gold (in save editor = 999999) seems to not use top byte.