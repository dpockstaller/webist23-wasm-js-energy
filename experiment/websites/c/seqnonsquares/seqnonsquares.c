/* based on: https://rosettacode.org/wiki/Sequence_of_non-squares#C (2022-01-04) */

#include <math.h>
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int nonsqr(int n) {
  return n + (int)round(sqrt(n));
}

EMSCRIPTEN_KEEPALIVE
int run_seqnonsquares(int *seq, int max) {
  for (int i = 0; i < max; i++) {
    seq[i] = nonsqr(i);
  }
  return 0;
}
