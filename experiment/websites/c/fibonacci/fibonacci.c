/* based on: https://rosettacode.org/wiki/Fibonacci_sequence#Recursive_33 (2021-12-29) */
/* converted JS version to C, as Rosetta Code C version is optimized */

#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int fibonacci(int n) {
   return (n < 2) ? n : fibonacci(n-1) + fibonacci(n-2);
}
