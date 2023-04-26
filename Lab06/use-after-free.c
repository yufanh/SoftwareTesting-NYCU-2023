#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv){

    long unsigned *useMe = malloc(sizeof(long unsigned));
    *useMe = 1234567890;
    printf("use befor free: %lu\n", *useMe);
    free(useMe);
    printf("use after free: %lu\n", *useMe);
    return 0;
}