/* based on: https://rosettacode.org/wiki/N-queens_problem#C (2021-12-24) */

//#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <emscripten/emscripten.h>

typedef uint32_t uint;
uint full, *qs, count = 0;

void solve(uint d, uint c, uint l, uint r) {
	uint b, a, *s;
	if (!d) {
		count++;
		return;
	}

	a = (c | (l <<= 1) | (r >>= 1)) & full;
	if (a != full)
		for (*(s = qs + --d) = 0, b = 1; b <= full; (*s)++, b <<= 1)
			if (!(b & a)) solve(d, b|c, b|l, b|r);
}

EMSCRIPTEN_KEEPALIVE
int run_nqueens(int n) {
	qs = calloc(n, sizeof(int));
	full = (1U << n) - 1;

	solve(n, 0, 0, 0);
	//log solutions count
	//printf("\nSolutions: %d\n", count);
	return 0;
}
