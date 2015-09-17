
#include "mbed.h"

Serial pc(USBTX, USBRX);

int main()
{
    pc.baud(115200);
    char msg[] = {'A','B'};
    int cnt = 0;

    while(1){
        pc.putc(msg[cnt%2]);
        wait(1);
        cnt++;
    }
}
