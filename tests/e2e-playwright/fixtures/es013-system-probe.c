/* ES-013 : routines natives, tampons éphémères et cinq fenêtres hors écran. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
void run(void) {
    *(volatile u16 *)0x4000208 = 0;
    *(volatile u16 *)0x4000000 = 0x403;
    volatile u32 *p = (u32 *)0x202f000;
    volatile u32 *result = (u32 *)0x202e000;
    volatile u8 *tiles = (u8 *)0x2038000;
    volatile u8 *window = (u8 *)0x20204b4;
    volatile u8 *expanded = (u8 *)0x202d004;
    for (int i = 0; i < 20480; i++) tiles[i] = 0;
    for (int i = 0; i < 60; i++) window[i] = 0;
    for (int i = -4; i < 516; i++) expanded[i] = 0xa5;
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors = (u8 *)0x202f100;
    colors[0] = 0; colors[1] = 1; colors[2] = 2;
    ((void (*)(void))0x813cc91)();
    for (int i = 0; i < 4; i++)
        ((void (*)(int, u32))0x813ccad)(i, 0x202f200 + i * 16);
    ((u32 (*)(u32, u32))0x813ccc9)((u32)expanded, p[0]);
    int length = 0;
    while (length < 512 && expanded[length] != 255) length++;
    result[0] = length + 1;
    result[1] = 1;
    for (int i = -4; i < 0; i++) if (expanded[i] != 0xa5) result[1] = 0;
    for (int i = length + 1; i < 516; i++) if (expanded[i] != 0xa5) result[1] = 0;
    int start = 0;
    for (int n = 0; n < 5; n++) {
        int width = n == 1 ? 240 : n == 0 ? 224 : 208;
        int font = n < 2 ? 0 : 2;
        int x = n < 2 ? 8 : 0;
        window[n * 12 + 3] = width / 8;
        window[n * 12 + 4] = 4;
        *(volatile u32 *)(window + n * 12 + 8) = (u32)tiles + n * 4096;
        u32 text;
        if (n < 2) text = p[n + 1];
        else {
            /* FB reste dans l'expansion vérifiée. La capture montre chaque
               page isolée, sans simuler une connexion réseau multijoueur. */
            volatile u8 *page = (u8 *)0x202c000;
            int i = 0;
            while (start < length && expanded[start] != 0xfb)
                page[i++] = expanded[start++];
            page[i] = 255;
            start++;
            text = (u32)page;
        }
        result[4 + n] = ((int (*)(int, u32, int))0x8005ed5)(font, text, 0);
        ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
            (n, font, x, 2, (u32)colors, 255, text);
    }
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int n = y / 32, row = y % 32;
        int width = n == 1 ? 240 : n == 0 ? 224 : 208;
        int pixel = 0;
        if (x < width) {
            int tile = (row / 8) * (width / 8) + x / 8;
            int byte = tiles[n * 4096 + tile * 32 + (row % 8) * 4 + (x % 8) / 2];
            pixel = (byte >> ((x % 2) * 4)) & 15;
        }
        screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    result[31] = 0x1044;
    for (;;) {}
}
