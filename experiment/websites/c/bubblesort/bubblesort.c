/* based on: http://rosettacode.org/wiki/Sorting_algorithms/Bubble_sort#C (2021-12-13) */

#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void bubblesort (int *a, int n) {
    int i, t, j = n, s = 1;
    while (s) {
        s = 0;
        for (i = 1; i < j; i++) {
            if (a[i] < a[i - 1]) {
                t = a[i];
                a[i] = a[i - 1];
                a[i - 1] = t;
                s = 1;
            }
        }
        j--;
    }
}
