/* Mire temporaire : lectures natives, GetStringWidth et AddTextPrinter. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
void run(void) {
    *(volatile u16 *)0x4000208 = 0;
    *(volatile u16 *)0x4000000 = 0x403;
    volatile u32 *params = (u32 *)0x202f000;
    volatile u32 *result = (u32 *)0x202e000;
    volatile u8 *window = (u8 *)0x20204b4;
    volatile u8 *tiles = (u8 *)0x2038000;
    for (int i = 0; i < 19200; i++) tiles[i] = 0;
    for (int i = 0; i < 12; i++) window[i] = 0;
    window[3] = 30;
    window[4] = 20;
    *(volatile u32 *)(window + 8) = (u32)tiles;
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors = (u8 *)0x202f100;
    colors[0] = 0; colors[1] = 1; colors[2] = 2;
    u32 target = *(volatile u32 *)params[0];
    int font = params[1];
    int width = ((int (*)(int, u32, int))0x8005ed5)(font, target, 0);
    result[0] = target;
    result[1] = width;
    result[2] = params[3];
    result[3] = params[4];
    if (width > (int)params[2]) {
        result[7] = 0xbad;
        for (;;) {}
    }
    ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
        (0, font, params[3], params[4], (u32)colors, 255, target);
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int tile = (y / 8) * 30 + x / 8;
        int byte = tiles[tile * 32 + (y % 8) * 4 + (x % 8) / 2];
        int pixel = (byte >> ((x % 2) * 4)) & 15;
        screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    result[7] = 0x1041;
    for (;;) {}
}
