/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Gnome_sort#C (2021-12-23) */

#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void gnomesort(int *a, int n)
{
  int i=1, j=2, t;
# define swap(i, j) { t = a[i]; a[i] = a[j]; a[j] = t; }
  while(i < n) {
    if (a[i - 1] > a[i]) {
      swap(i - 1, i);
      if (--i) continue;
    }
    i = j++;
  }
# undef swap
}
