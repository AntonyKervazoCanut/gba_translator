/* Sonde RAM : indexation des deux tables livrées, copie et impression natives. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
void run(void) {
    *(volatile u16 *)0x4000208 = 0;
    *(volatile u16 *)0x4000000 = 0x403;
    volatile u32 *result = (u32 *)0x202e000;
    u32 id = *(volatile u32 *)0x202f000;
    volatile u8 *tiles = (u8 *)0x2038000;
    volatile u8 *window = (u8 *)0x20204b4;
    for (int i = 0; i < 19200; i++) tiles[i] = 0;
    for (int i = 0; i < 24; i++) window[i] = 0;
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors = (u8 *)0x202f100;
    colors[0] = 0; colors[1] = 1; colors[2] = 2;
    for (u32 table = 0; table < 2; table++) {
        u32 target = ((volatile u32 *)(table ? 0x9fe65f4 : 0x8463e60))[id];
        volatile u8 *buffer = (u8 *)(0x202d004 + table * 32);
        for (int i = -4; i < 28; i++) buffer[i] = 0xa5;
        ((u32 (*)(u32, u32))0x8008d85)((u32)buffer, target);
        result[table * 4] = target;
        result[table * 4 + 1] = ((int (*)(int, u32, int))0x8005ed5)(0, (u32)buffer, 0);
        result[table * 4 + 2] = ((int (*)(int, u32, int))0x8005ed5)(2, (u32)buffer, 0);
        window[table * 12 + 3] = 30;
        window[table * 12 + 4] = 2;
        *(volatile u32 *)(window + table * 12 + 8) = (u32)tiles + table * 4096;
        ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
            (table, 2, 0, 0, (u32)colors, 255, (u32)buffer);
    }
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int pixel = 0;
        if (y < 16 || (y >= 32 && y < 48)) {
            int row = y < 16 ? y : y - 32;
            int base = y < 16 ? 0 : 4096;
            int tile = (row / 8) * 30 + x / 8;
            int byte = tiles[base + tile * 32 + (row % 8) * 4 + (x % 8) / 2];
            pixel = (byte >> ((x % 2) * 4)) & 15;
        }
        screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    result[31] = 0x1044;
    for (;;) {}
}
