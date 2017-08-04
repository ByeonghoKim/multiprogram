# multiprogram


###################################

numa.c compile needed
gcc -fPIC -shared -o numa.so numa.c -lnuma

wrapper.py reads text file and parse automatically

./wrapper.py -s $(TEXTFILE)

---------------------------------
10 0 ./stream 1000
20 1 ./hello 200
---------------------------------

wrapper reads file like...

bind core to 10, bind memory node to 0, argv[0] = ./stream, argv[1] = 1000
bind core to 20, bind memory node to 1, argv[0] = ./hello, argv[1] = 200

###################################
