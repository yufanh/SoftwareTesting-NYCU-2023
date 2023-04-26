#include <stdio.h>
#include <stdlib.h>

long unsigned *useMe;
void return_test(){
    long unsigned a = 987654321;
    useMe = &a;
    printf("use befor free: %lu\n", *useMe);
}
int main(int argc, char** argv){

    return_test();
    printf("use after return: %lu\n", *useMe);
    return 0;
}