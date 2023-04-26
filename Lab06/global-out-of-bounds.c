#include <stdio.h>
#include <stdlib.h>

int ARRAY[3];

int main(int argc, char** argv){
    unsigned size = 3;
    unsigned out_bounds = 1;

    printf("ARRAY size: %u\n", size);
    printf("ARRAY type: %s\n", "int");
    
    
    for(unsigned i = 0; i < size + out_bounds; i++){
        /* write out of bounds*/
        ARRAY[i] = i + 1;
        
        printf("ARRAY[%u]: %d", i, ARRAY[i]);

        /* read out of bounds*/
        if(i >= size) printf("  (Global out of bounds !)");

        printf("\n");
    }
    return 0;
}