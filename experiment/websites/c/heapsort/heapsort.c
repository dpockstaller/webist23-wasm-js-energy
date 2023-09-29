/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Heapsort#C (2021-12-23) */

#include <emscripten/emscripten.h>

int max (int *a, int n, int i, int j, int k) {
  int m = i;
  if (j < n && a[j] > a[m]) {
    m = j;
  }
  if (k < n && a[k] > a[m]) {
    m = k;
  }
  return m;
}

void downheap (int *a, int n, int i) {
  while (1) {
    int j = max(a, n, i, 2 * i + 1, 2 * i + 2);
    if (j == i) {
      break;
    }
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
    i = j;
  }
}

EMSCRIPTEN_KEEPALIVE
void heapsort (int *a, int n) {
  int i;
  for (i = (n - 2) / 2; i >= 0; i--) {
    downheap(a, n, i);
  }
  for (i = 0; i < n; i++) {
    int t = a[n - i - 1];
    a[n - i - 1] = a[0];
    a[0] = t;
    downheap(a, n - i - 1, 0);
  }
}
