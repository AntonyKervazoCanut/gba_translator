/* Sonde RAM sans sauvegarde : expansion et impression du moteur original. */
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
    u32 target = *(volatile u32 *)p[0];
    u32 font = p[1], width = p[2], bufferLength = p[3];
    for (int i = 0; i < 19200; i++) tiles[i] = 0;
    for (int i = 0; i < 24; i++) window[i] = 0;
    for (int n = 0; n < 2; n++) {
        window[n * 12 + 3] = width / 8;
        window[n * 12 + 4] = 2;
        *(volatile u32 *)(window + n * 12 + 8) = (u32)tiles + n * 4096;
    }
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors = (u8 *)0x202f100;
    colors[0] = 0; colors[1] = 1; colors[2] = 2;
    volatile u8 *expanded = (u8 *)0x202d000;
    for (int i = 0; i < 256; i++) expanded[i] = 0xa5;
    u32 text = target;
    u32 pcGuards = 0;
    if (bufferLength && p[5]) {
        /* Appel du vrai lecteur PC : il choisit le tampon par le type de
           table, expanse F7 puis imprime fenêtre1 police1 x0 y2. */
        volatile u8 *pc = (u8 *)0x2010000;
        for (int i = 0; i < 0x62bc; i++) pc[i] = 0;
        *(volatile u32 *)0x20397b0 = (u32)pc;
        for (int i = -4; i < 80; i++) pc[0x2180 + i] = 0xa5;
        for (u32 i = 0; i < bufferLength; i++) {
            pc[0xcea + i] = ((volatile u8 *)0x202f200)[i];
            pc[0x21d0 + i] = ((volatile u8 *)0x202f200)[i];
            pc[0xd61 + i] = ((volatile u8 *)0x202f200)[i];
        }
        if (bufferLength > 11) {
            pc[1] = 3; pc[0x21fe] = 2; pc[0x2200] = 1;
            *(volatile u16 *)(pc + 0x2224) = 716; /* Strawberry Sweet réel. */
        }
        const u8 *descriptor = (const u8 *)0x83cea38;
        for (int i = 0; i < 8; i++) window[12 + i] = descriptor[i];
        *(volatile u32 *)(window + 20) = (u32)tiles;
        /* Le champ 21D0 est un surnom vivant, pas un canari libre : garder
           son préimage complète jusqu'au prochain tampon légitime 21DB. */
        u8 neighbor[11];
        for (int i = 0; i < 11; i++) neighbor[i] = pc[0x21d0 + i];
        ((void (*)(u32))0x808fba5)(p[4]);
        pcGuards = 3;
        for (int i = 0; i < 4; i++)
            if (pc[0x217c + i] != 0xa5) pcGuards &= ~1u;
        for (int i = 0; i < 11; i++)
            if (pc[0x21d0 + i] != neighbor[i]) pcGuards &= ~2u;
        for (int i = 0; i < 80; i++) expanded[i] = pc[0x2180 + i];
        text = (u32)expanded;
    } else if (bufferLength) {
        ((void (*)(void))0x813cc91)();
        ((void (*)(int, u32))0x813ccad)(0, 0x202f200);
        ((u32 (*)(u32, u32))0x813ccc9)((u32)expanded, target);
        text = (u32)expanded;
    }
    int textWidth = ((int (*)(int, u32, int))0x8005ed5)(font, text, 0);
    int x = bufferLength ? 0 : 8;
    result[0] = target; result[1] = textWidth; result[2] = width;
    result[3] = x; result[4] = 0; result[5] = 0; result[6] = pcGuards;
    if (!bufferLength || !p[5])
        ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
            (0, font, x, 2, (u32)colors, 255, text);
    /* Le suffixe est imprimé indépendamment dans fenêtre1 à la colonne
       attendue. Son bitmap doit égaler celui produit par FC13/FC06. */
    if (!bufferLength) {
        const u8 *raw = (u8 *)text;
        for (int i = 0; i < 512 && raw[i] != 255; i++) {
            if (raw[i] == 0xfc && raw[i + 1] == 0x06) { font = raw[i + 2] & 15; i += 2; }
            else if (raw[i] == 0xfc && raw[i + 1] == 0x13) {
                result[4] = x + raw[i + 2];
                result[5] = (u32)(raw + i + 3);
                ((void (*)(int, int, int, int, u32, int, u32))0x812e51d)
                    (1, font, result[4], 2, (u32)colors, 255, result[5]);
                break;
            }
        }
    }
    volatile u16 *screen = (u16 *)0x6000000;
    for (int y = 0; y < 160; y++) for (int x = 0; x < 240; x++) {
        int pixel = 0;
        if (x < (int)width && (y < 16 || (y >= 32 && y < 48))) {
            int row = y < 16 ? y : y - 32;
            int base = y < 16 ? 0 : 4096;
            int tile = (row / 8) * (width / 8) + x / 8;
            int byte = tiles[base + tile * 32 + (row % 8) * 4 + (x % 8) / 2];
            pixel = (byte >> ((x % 2) * 4)) & 15;
        }
        if (bufferLength && p[5])
            screen[y * 240 + x] = pixel == 2 ? 0 : pixel == 3 ? 0x4210 : 0x7fff;
        else
            screen[y * 240 + x] = pixel == 1 ? 0 : pixel == 2 ? 0x4210 : 0x7fff;
    }
    result[31] = 0x1040;
    for (;;) {}
}
