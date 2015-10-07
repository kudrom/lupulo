
#include "mbed.h"

Serial pc(USBTX, USBRX);

int main()
{
    pc.baud(115200);
    int msg[] = {50,75};
    int cnt = 0;
    
    LocalFileSystem local("local");
    FILE *fp = fopen("/local/out.txt", "w");
    fclose(fp);

    while(1){
        pc.printf("{\"id\": 1, \"battery\": %d}\n", msg[cnt%2]);
        wait(1);
        cnt++;
    }
}
