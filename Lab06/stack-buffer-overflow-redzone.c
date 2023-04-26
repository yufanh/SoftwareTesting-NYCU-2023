#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv){
    unsigned size = 3;
    unsigned arr_1[3];
    unsigned arr_2[3];

    for (unsigned i = 0; i < size; i++) {
        arr_1[i] = 0;
        arr_2[i] = 123456789;
    }
    unsigned gap = &arr_2[0] -&arr_1[2];

    printf("stack buffer overflow redzone: %u\n", arr_1[2 + gap]);

    return 0;
}