/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Insertion_sort#C (2021-12-23) */

#include <stdio.h>
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void insertionsort(int *a, int n) {
	for(size_t i = 1; i < n; ++i) {
		int tmp = a[i];
		size_t j = i;
		while(j > 0 && tmp < a[j - 1]) {
			a[j] = a[j - 1];
			--j;
		}
		a[j] = tmp;
	}
}
