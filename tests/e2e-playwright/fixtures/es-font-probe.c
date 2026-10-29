typedef unsigned short u16;
typedef unsigned char u8;
void run(void) {
 *(volatile u16*)0x4000208=0;
 *(volatile u16*)0x4000000=0x403;
 volatile u16 *screen=(u16*)0x6000000;
 for(int i=0;i<240*160;i++)screen[i]=0x7fff;
 ((void(*)(int,int,int))0x8002ea9)(1,0,2);
 volatile unsigned *params=(unsigned*)0x202f000;
 for(int font=0;font<5;font++) {
  for(int n=0;n<16;n++) {
   ((void(*)(int,int))params[font])(params[5+n],0);
   volatile u8 *g=(u8*)0x3003da0;
   for(int y=0;y<16;y++)for(int x=0;x<16;x++) {
    int tile=(y/8)*2+x/8;
    int b=g[tile*32+(y%8)*4+(x%8)/2];
    int p=(b>>((x%2)*4))&15;
    screen[(4+font*18+y)*240+4+n*14+x]=(p==1?0:p==2?0x4210:0x7fff);
   }
  }
 }
 // Les badges utilisent leurs tuiles 4bpp réelles, décompressées par le BIOS.
 for(int block=0;block<4;block++) {
  unsigned src=params[21+block],dest=0x2038000;
  __asm__ volatile("movs r0,%0\n movs r1,%1\n swi 0x11"::"r"(src),"r"(dest):"r0","r1","r2","r3","memory");
  volatile u8 *tiles=(u8*)dest;
  for(int slot=0;slot<7;slot++)for(int y=0;y<8;y++)for(int x=0;x<32;x++) {
   int b=tiles[slot*128+(x/8)*32+y*4+(x%8)/2];
   int p=(b>>((x%2)*4))&15;
   screen[(96+block*10+y)*240+4+slot*33+x]=p==2?0:p==9?0x4210:0x7fff;
  }
 }
 // Bande de version réellement injectée dans le tileset NOT FOR SALE.
 unsigned src=*(volatile unsigned*)0x80ec610,dest=0x2038000;
 __asm__ volatile("movs r0,%0\n movs r1,%1\n swi 0x11"::"r"(src),"r"(dest):"r0","r1","r2","r3","memory");
 volatile u8 *tiles=(u8*)dest;
 for(int y=0;y<16;y++)for(int x=0;x<48;x++) {
  int tile=0xe1+(y/8)*6+x/8;
  int b=tiles[tile*32+(y%8)*4+(x%8)/2];
  int p=(b>>((x%2)*4))&15;
  screen[(140+y)*240+96+x]=p==4?0:0x7fff;
 }
 *(volatile unsigned*)0x202eff0=0x850;
 for(;;){}
}
