# Emscripten C compilation
Used Emscripten version: 3.1.1

### bubblesort
```bash
emcc bubblesort.c -s WASM=1 -o bubblesort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### quicksort
```bash
emcc quicksort.c -s WASM=1 -o quicksort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### mergesort
```bash
emcc mergesort.c -s WASM=1 -o mergesort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### insertionsort
```bash
emcc insertionsort.c -s WASM=1 -o insertionsort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### countingsort
```bash
emcc countingsort.c -s WASM=1 -o countingsort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### heapsort
```bash
emcc heapsort.c -s WASM=1 -o heapsort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### shellsort
```bash
emcc shellsort.c -s WASM=1 -o shellsort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### gnomesort
```bash
emcc gnomesort.c -s WASM=1 -o gnomesort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### pancakesort
```bash
emcc pancakesort.c -s WASM=1 -o pancakesort.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### kmeans++
```bash
emcc kmeanspp.c -s WASM=1 -o kmeanspp.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```

### happynumbers
```bash
emcc happynumbers.c -s WASM=1 -o happynumbers.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['cwrap']"
```

### perfectnumbers
```bash
emcc perfectnumbers.c -s WASM=1 -o perfectnumbers.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['cwrap']"
```

### humblenumbers
```bash
emcc humblenumbers.c -s WASM=1 -o humblenumbers.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['cwrap']"
```

### sequence non squares
```bash
emcc seqnonsquares.c -s WASM=1 -o seqnonsquares.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']" -s INITIAL_MEMORY=28MB
```

### nqueens
```bash
emcc nqueens.c -s WASM=1 -o nqueens.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']"
```

### fibonacci
```bash
emcc fibonacci.c -s WASM=1 -o fibonacci.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']"
```

### ackermann
```bash
emcc ackermann.c -s WASM=1 -o ackermann.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']"
```

### towers of hanoi
```bash
emcc towersofhanoi.c -s WASM=1 -o towersofhanoi.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']"
```

### matrix multiplication
```bash
emcc matrixmultiplication.c -s WASM=1 -o matrixmultiplication.js -s NO_EXIT_RUNTIME=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['ccall']" -s "EXPORTED_FUNCTIONS=['_malloc','_free']"
```
