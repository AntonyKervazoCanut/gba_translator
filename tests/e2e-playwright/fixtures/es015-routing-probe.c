/* Mire RAM : consommateurs ROM, expansion FD et impression natives.
 * Les pages sont présentées en lignes séparées ; ce n'est pas un parcours de jeu. */
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
    volatile u8 *name = (u8 *)0x202f200;
    for (int i=0;i<7;i++) name[i]=0xc7; /* MMMMMMM : fixture uniquement. */
    name[7]=0xff;
    /* FD02 : tampon temporaire borné à cinq glyphes, comme sir/madam ES-016. */
    for (int i=0;i<5;i++) ((volatile u8 *)0x2021cd0)[i]=0xc7;
    ((volatile u8 *)0x2021cd0)[5]=0xff;
    *(volatile u32 *)0x300500c=(u32)name;
    u8 *text=(u8 *)0x202a000;
    u8 *line=(u8 *)0x202a400;
    volatile u8 *ref=(u8 *)params[0];
    u32 target=ref[0]|(ref[1]<<8)|(ref[2]<<16)|(ref[3]<<24);
    ((u8 *(*)(u8 *,u32))0x8008fcd)(text,target);
    for(int i=0;i<19200;i++)tiles[i]=0;
    for(int i=0;i<12;i++)window[i]=0;
    window[3]=30; window[4]=20;
    *(volatile u32 *)(window+8)=(u32)tiles;
    ((void (*)(u32))0x8002c1d)(0x841f444);
    volatile u8 *colors=(u8 *)0x202f100;
    colors[0]=0; colors[1]=1; colors[2]=2;
    int count=0,length=0;
    for(int i=0;i<512;i++) {
        int value=text[i];
        if(value==0xfe || value==0xfa || value==0xfb || value==0xff) {
            line[length]=0xff;
            int width=((int (*)(int,u32,int))0x8005ed5)(2,(u32)line,0);
            result[4+count]=width;
            if(count<7) ((void (*)(int,int,int,int,u32,int,u32))0x812e51d)
                (0,2,4,4+20*count,(u32)colors,255,(u32)line);
            count++; length=0;
            if(value==0xff)break;
        } else {
            line[length++]=value;
            if(value==0xfc) {line[length++]=text[++i];line[length++]=text[++i];}
            else if(value==0xf8 || value==0xf9)line[length++]=text[++i];
        }
    }
    volatile u16 *screen=(u16 *)0x6000000;
    for(int y=0;y<160;y++)for(int x=0;x<240;x++) {
        int tile=(y/8)*30+x/8;
        int byte=tiles[tile*32+(y%8)*4+(x%8)/2];
        int pixel=(byte>>((x%2)*4))&15;
        screen[y*240+x]=pixel==0?0x7fff:pixel==2?0x4210:0;
    }
    result[0]=0x1043;result[1]=target;result[2]=count;
    for(;;){}
}
