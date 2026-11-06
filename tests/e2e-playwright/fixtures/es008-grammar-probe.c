/* Sonde jetable : vrai BufferStringBattle, puis vrai décompresseur de police. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned u32;
void run(void) {
 *(volatile u16*)0x4000208=0;
 *(volatile u16*)0x4000128=0;
 for (u32 p=0x2000000;p<0x2040000;p+=4) *(volatile u32*)p=0;
 volatile u32 *params=(u32*)0x09fff800;
 for(int n=0;n<7;n++) {
  *(volatile u32*)0x2039a34=0x2022bc8;
  *(volatile u32*)0x2023fe8=0x203b000;
  *(volatile u16*)0x2022bc8=params[n*2];
  *(volatile u8*)0x2022bd4=params[n*2+1];
  for(int k=0;k<10;k++) ((volatile u8*)0x202428c)[k]=0xbb+k;
  *(volatile u8*)0x2024296=0xff;
  for(int k=0;k<256;k++) ((volatile u8*)0x202298c)[k]=0xa5;
  ((void(*)(int))0x80d7275)(4);
  for(int k=0;k<256;k++) ((volatile u8*)(0x203c000+n*256))[k]=((volatile u8*)0x202298c)[k];
 }
 *(volatile u16*)0x4000000=0x403;
 volatile u16 *screen=(u16*)0x6000000;
 for(int i=0;i<240*160;i++)screen[i]=0x7fff;
 ((void(*)(int,int,int))0x8002ea9)(1,0,2);
 for(int n=0;n<5;n++) {
  volatile u8 *text=(u8*)(0x203c000+n*256);
  int x=4,y=n*32;
  for(int k=0;k<255 && text[k]!=0xff;k++) {
   int cp=text[k];
   if(cp==0xfe){x=4;y+=16;continue;}
   ((void(*)(int,int))0x80065b9)(cp,0);
   volatile u8 *g=(u8*)0x3003da0;
   for(int dy=0;dy<16;dy++)for(int dx=0;dx<8;dx++) {
    int b=g[(dy/8)*64+(dy%8)*4+dx/2];
    int pixel=(b>>((dx%2)*4))&15;
    if(pixel==1 || pixel==2)screen[(y+dy)*240+x+dx]=(pixel==1?0:0x4210);
   }
   x+=((volatile u8*)params[14])[cp];
  }
 }
 *(volatile u32*)0x202eff0=0x1038;
 for(;;){}
}
