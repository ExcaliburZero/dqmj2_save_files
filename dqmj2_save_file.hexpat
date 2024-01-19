struct monster {
    u8 name[0x10]; // Most characters are 1 byte, might be some that can be 2 bytes, have not confirmed
    u8 unknown_1[0x4];
    u32 id; // Not sure the semantics of this, need to confirm
    u16 race_id; // species
    u8 sex; // 0=M, 1=F, 2=N
    u8 synthesis_count;
    u8 unknown_2;
    u8 level_cap; // 0=lv50, 1=lv75, 2=lv100, need to confirm
};

u24 magic @ 0x00;
u32 data_checksum @ 0x88;
u32 header_checksum @ 0x8C;
u32 play_time_frames @ 0x90;
u8 player_name[0x08] @ 0x98;
u32 gold @ 0xAC;
u32 atm @ 0xB0;
u16 victories @ 0x1DC;
u16 scout_count @ 0x1DE;
u16 synthesis_count @ 0x1E0;
u8 has_zoom @ 0x1D8;
u8 has_zip @ 0x1D9;
u8 has_nose_for_treasure @ 0x1DA;
u8 has_vanish @ 0x1DB;
u8 can_scout_huge_monsters @ 0x3F02;
u8 save_location_id @ 0x3FCC;
s32 save_location_x @ 0x3FD4;
s32 save_location_y @ 0x3FD8;
s32 save_location_z @ 0x3FDC;
u8 menu_commands[0x0C] @ 0x1CC [[comment("Re-orderable icons on the player's menu. (ex. Save, Equipment, etc.)")]];
monster first_party_monster @ 0x1E8;