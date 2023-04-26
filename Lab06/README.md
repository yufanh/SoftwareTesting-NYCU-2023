NYCU-Software-Testing-2023 Lab06
===

### Environment
* Ubuntu: Ubuntu22.04(WSL2)
    * 5.15.90.1-microsoft-standard-WSL2
* gcc:
    * gcc version 11.3.0 (Ubuntu 11.3.0-1ubuntu1~22.04)
* valgrind:
    * valgrind-3.18.1

| test case             | Valgrind | ASAN     |
| --------------------- | -------- | -------- |
| Heap out-of-bounds    | Yes      | Yes      |
| Stack out-of-bounds   | No       | Yes      |
| Global out-of-bounds  | No       | Yes      |
| Use-after-free        | Yes      | Yes      |
| Use-after-return      | Yes      | Yes      |


## 1-1 Heap out-of-bounds read/write
### heap-out-of-bounds.c

```c=
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char** argv){
    unsigned size = 3;
    unsigned out_bounds = 1;
    int *arr = malloc(sizeof(int) * size);

    printf("arr size: %u\n", size);
    printf("arr type: %s\n", "int");
    
    
    for(unsigned i = 0; i < size + out_bounds; i++){
        /* write out of bounds*/
        *(arr + i) = i + 1;
        
        printf("arr[%u]: %d", i, arr[i]);

        /* read out of bounds*/
        if(i >= size) printf("  (Heap out of bounds !)");

        printf("\n");
    }
    return 0;
}
```
### ASan report
```
$ gcc -fsanitize=address -O1 -g -o heap_test heap-out-of-bounds.c
$ ./heap_test
arr size: 3
arr type: int
arr[0]: 1
arr[1]: 2
arr[2]: 3
=================================================================
==4444==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000001c at pc 0x556527eca318 bp 0x7ffc528d7010 sp 0x7ffc528d7000
WRITE of size 4 at 0x60200000001c thread T0
    #0 0x556527eca317 in main /home/fan/software_testing_2023/06_lab/heap-out-of-bounds.c:14
    #1 0x7f80fef12d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f80fef12e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x556527eca164 in _start (/home/fan/software_testing_2023/06_lab/heap_test+0x1164)

0x60200000001c is located 0 bytes to the right of 12-byte region [0x602000000010,0x60200000001c)
allocated by thread T0 here:
    #0 0x7f80ff1c5867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x556527eca23e in main /home/fan/software_testing_2023/06_lab/heap-out-of-bounds.c:6

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/fan/software_testing_2023/06_lab/heap-out-of-bounds.c:14 in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa 00[04]fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4444==ABORTING

```
### valgrind report
```
$ gcc -o heap_test heap-out-of-bounds.c
$ valgrind ./heap_test
==4478== Memcheck, a memory error detector
==4478== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4478== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4478== Command: ./heap_test
==4478==
arr size: 3
arr type: int
arr[0]: 1
arr[1]: 2
arr[2]: 3
==4478== Invalid write of size 4
==4478==    at 0x109215: main (in /home/fan/software_testing_2023/06_lab/heap_test)
==4478==  Address 0x4a8e04c is 0 bytes after a block of size 12 alloc'd
==4478==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==4478==    by 0x1091B8: main (in /home/fan/software_testing_2023/06_lab/heap_test)
==4478==
==4478== Invalid read of size 4
==4478==    at 0x109229: main (in /home/fan/software_testing_2023/06_lab/heap_test)
==4478==  Address 0x4a8e04c is 0 bytes after a block of size 12 alloc'd
==4478==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==4478==    by 0x1091B8: main (in /home/fan/software_testing_2023/06_lab/heap_test)
==4478==
arr[3]: 4  (Heap out of bounds !)
==4478==
==4478== HEAP SUMMARY:
==4478==     in use at exit: 12 bytes in 1 blocks
==4478==   total heap usage: 2 allocs, 1 frees, 1,036 bytes allocated
==4478==
==4478== LEAK SUMMARY:
==4478==    definitely lost: 12 bytes in 1 blocks
==4478==    indirectly lost: 0 bytes in 0 blocks
==4478==      possibly lost: 0 bytes in 0 blocks
==4478==    still reachable: 0 bytes in 0 blocks
==4478==         suppressed: 0 bytes in 0 blocks
==4478== Rerun with --leak-check=full to see details of leaked memory
==4478==
==4478== For lists of detected and suppressed errors, rerun with: -s
==4478== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)

```
**ASan 能, valgrind 能**



## 1-2 Stack out-of-bounds read/write
### stack-out-of-bounds.c
```c=
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
```
### ASan report
```
$ gcc -fsanitize=address -O1 -g -o stack_test stack-out-of-bounds.c
$ ./stack_test
arr size: 3
arr type: int
arr[0]: 1
arr[1]: 2
arr[2]: 3
=================================================================
==4218==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffed7be7dc at pc 0x5575a78823c5 bp 0x7fffed7be790 sp 0x7fffed7be780
WRITE of size 4 at 0x7fffed7be7dc thread T0
    #0 0x5575a78823c4 in main /home/fan/software_testing_2023/06_lab/stack-out-of-bounds.c:14
    #1 0x7f4569dcbd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f4569dcbe3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x5575a7882184 in _start (/home/fan/software_testing_2023/06_lab/stack_test+0x1184)

Address 0x7fffed7be7dc is located in stack of thread T0 at offset 44 in frame
    #0 0x5575a7882258 in main /home/fan/software_testing_2023/06_lab/stack-out-of-bounds.c:3

  This frame has 1 object(s):
    [32, 44) 'arr' (line 6) <== Memory access at offset 44 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/fan/software_testing_2023/06_lab/stack-out-of-bounds.c:14 in main
Shadow bytes around the buggy address:
  0x10007daefca0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefcb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefcc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefcd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefce0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x10007daefcf0: 00 00 00 00 00 00 f1 f1 f1 f1 00[04]f3 f3 00 00
  0x10007daefd00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefd10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefd20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefd30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007daefd40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4218==ABORTING

```
### valgrind report
```
$ gcc -o stack_test stack-out-of-bounds.c
$ valgrind ./stack_test
==4252== Memcheck, a memory error detector
==4252== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4252== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4252== Command: ./stack_test
==4252==
arr size: 3
arr type: int
arr[0]: 1
arr[1]: 2
arr[2]: 3
arr[3]: 4  (Stack out of bounds !)
*** stack smashing detected ***: terminated
==4252==
==4252== Process terminating with default action of signal 6 (SIGABRT)
==4252==    at 0x48F9A7C: __pthread_kill_implementation (pthread_kill.c:44)
==4252==    by 0x48F9A7C: __pthread_kill_internal (pthread_kill.c:78)
==4252==    by 0x48F9A7C: pthread_kill@@GLIBC_2.34 (pthread_kill.c:89)
==4252==    by 0x48A5475: raise (raise.c:26)
==4252==    by 0x488B7F2: abort (abort.c:79)
==4252==    by 0x48EC6F5: __libc_message (libc_fatal.c:155)
==4252==    by 0x4999769: __fortify_fail (fortify_fail.c:26)
==4252==    by 0x4999735: __stack_chk_fail (stack_chk_fail.c:24)
==4252==    by 0x109277: main (in /home/fan/software_testing_2023/06_lab/stack_test)
==4252==
==4252== HEAP SUMMARY:
==4252==     in use at exit: 1,024 bytes in 1 blocks
==4252==   total heap usage: 1 allocs, 0 frees, 1,024 bytes allocated
==4252==
==4252== LEAK SUMMARY:
==4252==    definitely lost: 0 bytes in 0 blocks
==4252==    indirectly lost: 0 bytes in 0 blocks
==4252==      possibly lost: 0 bytes in 0 blocks
==4252==    still reachable: 1,024 bytes in 1 blocks
==4252==         suppressed: 0 bytes in 0 blocks
==4252== Rerun with --leak-check=full to see details of leaked memory
==4252==
==4252== For lists of detected and suppressed errors, rerun with: -s
==4252== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
[1]    4252 IOT instruction  valgrind ./stack_test

```
**ASan 能, valgrind 不能**

## 1-3 Global out-of-bounds read/write
### global-out-of-bounds.c
```c=
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
```
### ASan report
```
$ gcc -fsanitize=address -O1 -g -o global_test global-out-of-bounds.c
$ ./global_test
ARRAY size: 3
ARRAY type: int
ARRAY[0]: 1
ARRAY[1]: 2
ARRAY[2]: 3
=================================================================
==4307==ERROR: AddressSanitizer: global-buffer-overflow on address 0x56483711a1ec at pc 0x5648371172f6 bp 0x7ffc192c4550 sp 0x7ffc192c4540
WRITE of size 4 at 0x56483711a1ec thread T0
    #0 0x5648371172f5 in main /home/fan/software_testing_2023/06_lab/global-out-of-bounds.c:16
    #1 0x7f0003745d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f0003745e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x564837117144 in _start (/home/fan/software_testing_2023/06_lab/global_test+0x1144)

0x56483711a1ec is located 0 bytes to the right of global variable 'ARRAY' defined in 'global-out-of-bounds.c:4:5' (0x56483711a1e0) of size 12
SUMMARY: AddressSanitizer: global-buffer-overflow /home/fan/software_testing_2023/06_lab/global-out-of-bounds.c:16 in main
Shadow bytes around the buggy address:
  0x0ac986e1b3e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b3f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b400: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9
  0x0ac986e1b410: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x0ac986e1b420: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
=>0x0ac986e1b430: f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00[04]f9 f9
  0x0ac986e1b440: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b450: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac986e1b480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4307==ABORTING
```
### valgrind report
```
$ gcc -o global_test global-out-of-bounds.c
$ valgrind ./global_test
==4341== Memcheck, a memory error detector
==4341== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4341== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4341== Command: ./global_test
==4341==
ARRAY size: 3
ARRAY type: int
ARRAY[0]: 1
ARRAY[1]: 2
ARRAY[2]: 3
ARRAY[3]: 4  (Global out of bounds !)
==4341==
==4341== HEAP SUMMARY:
==4341==     in use at exit: 0 bytes in 0 blocks
==4341==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==4341==
==4341== All heap blocks were freed -- no leaks are possible
==4341==
==4341== For lists of detected and suppressed errors, rerun with: -s
==4341== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

**ASan 能, valgrind 不能**


## 1-4 Use-after-free
### use-after-free.c
```c=
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
```
### ASan report
```
$ gcc -fsanitize=address -O1 -g -o free_test use-after-free.c
$ ./free_test
use befor free: 1234567890
=================================================================
==5488==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x564c51d71296 bp 0x7fff7cfdcfd0 sp 0x7fff7cfdcfc0
READ of size 8 at 0x602000000010 thread T0
    #0 0x564c51d71295 in main /home/fan/software_testing_2023/06_lab/use-after-free.c:11
    #1 0x7f700a588d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f700a588e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x564c51d71164 in _start (/home/fan/software_testing_2023/06_lab/free_test+0x1164)

0x602000000010 is located 0 bytes inside of 8-byte region [0x602000000010,0x602000000018)
freed by thread T0 here:
    #0 0x7f700a83b517 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x564c51d7125d in main /home/fan/software_testing_2023/06_lab/use-after-free.c:9

previously allocated by thread T0 here:
    #0 0x7f700a83b867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x564c51d71237 in main /home/fan/software_testing_2023/06_lab/use-after-free.c:6

SUMMARY: AddressSanitizer: heap-use-after-free /home/fan/software_testing_2023/06_lab/use-after-free.c:11 in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa[fd]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==5488==ABORTING
```
### valgrind report
```
$ gcc -o free_test use-after-free.c
$ valgrind ./free_test
==5522== Memcheck, a memory error detector
==5522== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==5522== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==5522== Command: ./free_test
==5522==
use befor free: 1234567890
==5522== Invalid read of size 8
==5522==    at 0x1091E3: main (in /home/fan/software_testing_2023/06_lab/free_test)
==5522==  Address 0x4a8e040 is 0 bytes inside a block of size 8 free'd
==5522==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==5522==    by 0x1091DE: main (in /home/fan/software_testing_2023/06_lab/free_test)
==5522==  Block was alloc'd at
==5522==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==5522==    by 0x1091A5: main (in /home/fan/software_testing_2023/06_lab/free_test)
==5522==
use after free: 1234567890
==5522==
==5522== HEAP SUMMARY:
==5522==     in use at exit: 0 bytes in 0 blocks
==5522==   total heap usage: 2 allocs, 2 frees, 1,032 bytes allocated
==5522==
==5522== All heap blocks were freed -- no leaks are possible
==5522==
==5522== For lists of detected and suppressed errors, rerun with: -s
==5522== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

**ASan 能, valgrind 能**



## 1-5 Use-after-return
### use-after-return.c
```c=
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
```
### ASan report
> You need to run the test with ASAN_OPTIONS=detect_stack_use_after_return=1
> [AddressSanitizerExampleUseAfterReturn](https://github.com/google/sanitizers/wiki/AddressSanitizerExampleUseAfterReturn)(official github)
```
$ gcc -fsanitize=address -O1 -g -o return_test use-after-return.c
$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./return_test
use befor free: 987654321
=================================================================
==6151==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f04e4044020 at pc 0x562728a023b1 bp 0x7ffe75423900 sp 0x7ffe754238f0
READ of size 8 at 0x7f04e4044020 thread T0
    #0 0x562728a023b0 in main /home/fan/software_testing_2023/06_lab/use-after-return.c:13
    #1 0x7f04e77e0d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f04e77e0e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x562728a02184 in _start (/home/fan/software_testing_2023/06_lab/return_test+0x1184)

Address 0x7f04e4044020 is located in stack of thread T0 at offset 32 in frame
    #0 0x562728a02258 in return_test /home/fan/software_testing_2023/06_lab/use-after-return.c:5

  This frame has 1 object(s):
    [32, 40) 'a' (line 6) <== Memory access at offset 32 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /home/fan/software_testing_2023/06_lab/use-after-return.c:13 in main
Shadow bytes around the buggy address:
  0x0fe11c8007b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c8007c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c8007d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c8007e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c8007f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe11c800800: f5 f5 f5 f5[f5]f5 f5 f5 00 00 00 00 00 00 00 00
  0x0fe11c800810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c800820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c800830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c800840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe11c800850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==6151==ABORTING
```
### algrind report
```
$ gcc -o return_test use-after-return.c
$ valgrind ./return_test
==6185== Memcheck, a memory error detector
==6185== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==6185== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==6185== Command: ./return_test
==6185==
use befor free: 987654321
==6185== Use of uninitialised value of size 8
==6185==    at 0x48BD33B: _itoa_word (_itoa.c:177)
==6185==    by 0x48D8B3D: __vfprintf_internal (vfprintf-internal.c:1516)
==6185==    by 0x48C381E: printf (printf.c:33)
==6185==    by 0x10920C: main (in /home/fan/software_testing_2023/06_lab/return_test)
==6185==
==6185== Conditional jump or move depends on uninitialised value(s)
==6185==    at 0x48BD34C: _itoa_word (_itoa.c:177)
==6185==    by 0x48D8B3D: __vfprintf_internal (vfprintf-internal.c:1516)
==6185==    by 0x48C381E: printf (printf.c:33)
==6185==    by 0x10920C: main (in /home/fan/software_testing_2023/06_lab/return_test)
==6185==
==6185== Conditional jump or move depends on uninitialised value(s)
==6185==    at 0x48D9643: __vfprintf_internal (vfprintf-internal.c:1516)
==6185==    by 0x48C381E: printf (printf.c:33)
==6185==    by 0x10920C: main (in /home/fan/software_testing_2023/06_lab/return_test)
==6185==
==6185== Conditional jump or move depends on uninitialised value(s)
==6185==    at 0x48D8C85: __vfprintf_internal (vfprintf-internal.c:1516)
==6185==    by 0x48C381E: printf (printf.c:33)
==6185==    by 0x10920C: main (in /home/fan/software_testing_2023/06_lab/return_test)
==6185==
use after return: 987654321
==6185==
==6185== HEAP SUMMARY:
==6185==     in use at exit: 0 bytes in 0 blocks
==6185==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==6185==
==6185== All heap blocks were freed -- no leaks are possible
==6185==
==6185== Use --track-origins=yes to see where uninitialised values come from
==6185== For lists of detected and suppressed errors, rerun with: -s
==6185== ERROR SUMMARY: 20 errors from 4 contexts (suppressed: 0 from 0)
```

**ASan 能, valgrind 能**



## 2 Stack buffer overflow 剛好越過 redzone
### stack-buffer-overflow-redzone.c
```c=
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
```
### ASan report
```
$ gcc -fsanitize=address -O1 -g -o redzone_test stack-buffer-overflow-redzone.c
$ ./redzone_test
stack buffer overflow redzone: 123456789
```

**ASan 不能**

