/* based on: https://rosettacode.org/wiki/Ackermann_function#C (2022-01-14) */

#include <emscripten/emscripten.h>

int ackermann(int m, int n) {
  if (!m) return n + 1;
  if (!n) return ackermann(m - 1, 1);
  return ackermann(m - 1, ackermann(m, n - 1));
}

EMSCRIPTEN_KEEPALIVE
int run_ackermann(int x, int y) {
  for (int m = 0; m <= x; m++)
    for (int n = 0; n <= y; n++)
      ackermann(m, n);
  return 0;
}
