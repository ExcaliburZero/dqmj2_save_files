Info on the save data file format for Dragon Quest Monsters: Joker 2.

Re-reverse engineered from DQM Joker 2 Save Data Editor (created by asa-o, translated into English by Hynckel and jm_plata):

https://web.archive.org/web/20200303213846/http://www.asa-o.net/tools/dqmj2_cheat
https://www.woodus.com/den/games/dqm5ds/save_data_editor.php

## Format
* Binary
* Little endian

### Header [0x0 to 0x90]
#### Magic [0x0 to 0x2]
Magic bytes that indicate that this is a DQMJ2 save file.

```
SYN
```

#### Data checksum [0x88 to 0x8B]
Checksum of the data portion of the file.

32bit unsigned integer.

```python
def dqj2_checksum(data: list[bytes]) -> int:
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
# TODO: IIRC same checksum algorithm as data checksum, but on 0x0 to 0x8B
```

### Data [0x90 to 0x___]