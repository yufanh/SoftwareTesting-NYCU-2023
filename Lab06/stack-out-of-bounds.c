#include <stdio.h>
#include <stdlib.h>
int main(int argc, char** argv){
    unsigned size = 3;
    unsigned out_bounds = 1;
    int arr[3];

    printf("arr size: %u\n", size);
    printf("arr type: %s\n", "int");
    
    
    for(unsigned i = 0; i < size + out_bounds; i++){
        /* write out of bounds*/
        arr[i] = i + 1;
        
        printf("arr[%u]: %d", i, arr[i]);

        /* read out of bounds*/
        if(i >= size) printf("  (Stack out of bounds !)");

        printf("\n");
    }
    return 0;
}