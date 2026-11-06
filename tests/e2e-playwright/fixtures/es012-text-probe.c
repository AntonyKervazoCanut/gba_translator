/* Sonde RAM : métriques et imprimeur natifs, ROM et polices intactes. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

void run(void) {
    *(volatile u16 *)0x4000208 = 0;
    *(volatile u16 *)0x4000000 = 0x403;
    volatile u32 *params = (u32 *)0x202b000;
    volatile u32 *results = (u32 *)0x202d000;
    for (u32 n = 0; n < params[0]; n++) {
        u32 target = *(volatile u32 *)params[2 + n * 3];
        int width = ((int (*)(int, u32, int))0x8005ed5)(2, target, 0);
        volatile u8 *text = (u8 *)target;
        u32 length = 0, lines = 1;
        while (length < 512 && text[length] != 0xff) {
            if (text[length] == 0xfe) lines++;
            length++;
        }
        results[n * 4] = target;
        results[n * 4 + 1] = width;
        results[n * 4 + 2] = lines;
        results[n * 4 + 3] = length + 1;
        if (width > (int)params[3 + n * 3] || lines != params[4 + n * 3]
            || lines > 3 || length == 512) {
            *(volatile u32 *)0x202f000 = 0xbad;
            *(volatile u32 *)0x202f004 = n;
            for (;;) {}
        }
    }
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
    u32 target = results[params[1] * 4];
    ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
        (0, 2, 4, 4, (u32)colors, 255, target);
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int tile = (y / 8) * 30 + x / 8;
        int byte = tiles[tile * 32 + (y % 8) * 4 + (x % 8) / 2];
        int pixel = (byte >> ((x % 2) * 4)) & 15;
        screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    *(volatile u32 *)0x202f000 = 0x862;
    for (;;) {}
}
