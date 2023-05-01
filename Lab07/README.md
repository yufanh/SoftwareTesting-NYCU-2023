NYCU-Software-Testing-2023 Lab07
===
**Build & fuzz with AFL**
```shell=
$ cd Lab07
$ export CC=~/AFL/afl-gcc
$ export AFL_USE_ASAN=1
$ make
$ mkdir in
$ cp test.bmp in/
$ ~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```
![](https://i.imgur.com/TTKE9c0.jpg)

**PoC: the file that can trigger the vulnerability**
- Lab07/out/crashes/id:0000*
![](https://i.imgur.com/XM49L9R.png)


**ASAN error report**
```shell=
$ ./bmpgrayscale out/crashes/id:000000* a.bmp
```
![](https://i.imgur.com/oh8g4yk.jpg)

