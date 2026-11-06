/* F-859 : glyphes natifs et expansion FD ; aucune écriture ROM/sauvegarde. */
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
    volatile u8 *expanded = (u8 *)0x202d000;
    volatile u8 *page = (u8 *)0x202e800;
    result[6] = 0; result[7] = 0; result[8] = 0;
    /* Adresses prouvées par 9120/912C/9134/913C et leurs littéraux. */
    for (int n = 0; n < 3; n++) {
        u32 address = 0x2021cd0;
        if (n == 1) address += 0x20;
        if (n == 2) address += 0x34;
        volatile u8 *buffer = (u8 *)address;
        int length = p[3] ? 4 : 10;
        for (int i = 0; i < length; i++) buffer[i] = p[3] ? 0xaa : 0xd1;
        buffer[length] = 255;
    }
    *(volatile u32 *)0x300500c = 0x202f600;
    for (int i = 0; i < 7; i++) ((volatile u8 *)0x202f600)[i] = 0xd1;
    ((volatile u8 *)0x202f600)[7] = 255;
    if (p[4]) {
        /* Vrai handler de bufferstdstring, vers le plus petit tampon (20 o). */
        volatile u8 *buffer = (u8 *)0x2021d04;
        volatile u8 *copy = (u8 *)0x202ec00;
        for (int i = -4; i < 24; i++) buffer[i] = 0xa5;
        volatile u8 *operand = (u8 *)0x202f740;
        operand[0] = 2; operand[1] = p[4] - 1; operand[2] = 0;
        *(volatile u32 *)0x202f708 = (u32)operand;
        result[8] = ((int (*)(u32))0x806bed5)(0x202f700);
        int length = 0;
        while (length < 20 && buffer[length] != 255) {
            copy[length] = buffer[length]; length++;
        }
        copy[length] = 255;
        result[6] = length + 1;
        int guards = 3;
        for (int i = 0; i < 4; i++) {
            if (buffer[-4+i] != 0xa5) guards &= ~1u;
            if (buffer[20+i] != 0xa5) guards &= ~2u;
        }
        result[7] = guards;
    }
    for (int i = -4; i < 2052; i++) expanded[i] = 0xa5;
    ((void (*)(u32, u32))0x8008fcd)((u32)expanded, p[0]);
    int expandedLength = 0;
    while (expandedLength < 2048 && expanded[expandedLength] != 255) expandedLength++;
    /* Les pauses ne sont pas jouées dans cette vue de glyphes. Leur présence,
       leurs arguments et la pagination restent vérifiés sur les vraies sources. */
    int current = 0, length = 0;
    for (int i = 0; i < expandedLength; i++) {
        u8 value = expanded[i];
        if (value == 0xfb || value == 0xfa) { current++; continue; }
        if (value == 0xfc) {
            u8 command = expanded[++i];
            i += command == 8 ? 1 : command == 0x10 ? 2 : 0;
            continue;
        }
        if (current == (int)p[1] && length < 511) page[length++] = value;
    }
    page[length] = 255;
    for (int i = 0; i < 4096; i++) tiles[i] = 0;
    for (int i = 0; i < 24; i++) window[i] = 0;
    window[3] = 24; window[4] = 4;
    *(volatile u32 *)(window + 8) = (u32)tiles;
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors = (u8 *)0x202f100;
    colors[0] = 0; colors[1] = 1; colors[2] = 2;
    int width = ((int (*)(int, u32, int))0x8005ed5)(p[2], (u32)page, 0);
    ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
        (0, p[2], 0, 0, (u32)colors, 255, (u32)page);
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int pixel = 0;
        if (x < 192 && y < 32) {
            int tile = (y / 8) * 24 + x / 8;
            int byte = tiles[tile * 32 + (y % 8) * 4 + (x % 8) / 2];
            pixel = (byte >> ((x % 2) * 4)) & 15;
        }
        screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    int guards = 3;
    for (int i = 0; i < 4; i++) {
        if (expanded[-4+i] != 0xa5) guards &= ~1u;
        if (expanded[2048+i] != 0xa5) guards &= ~2u;
    }
    result[0] = p[0]; result[1] = width; result[2] = length;
    result[3] = expandedLength + 1; result[4] = guards;
    result[31] = 0xf859;
    for (;;) {}
}
