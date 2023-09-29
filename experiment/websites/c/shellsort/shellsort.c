/* based on: http://rosettacode.org/wiki/Sorting_algorithms/Bubble_sort#C (2021-12-13) */

#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void shellsort (int *a, int n) {
  int h, i, j, t;
  for (h = n; h /= 2;) {
    for (i = h; i < n; i++) {
      t = a[i];
      for (j = i; j >= h && t < a[j - h]; j -= h) {
        a[j] = a[j - h];
      }
      a[j] = t;
    }
  }
}
