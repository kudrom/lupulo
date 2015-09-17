
#include "mbed.h"

Serial pc(USBTX, USBRX);

int main()
{
    pc.baud(115200);

    while(1){
        pc.putc('.');
        wait(1);
    }
}
