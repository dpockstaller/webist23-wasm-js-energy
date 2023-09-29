/* based on: https://rosettacode.org/wiki/Happy_numbers#C (2021-12-23) */

//#include <stdio.h>
#include <emscripten/emscripten.h>

int dsum(int n) {
	int sum, x;
	for (sum = 0; n; n /= 10) x = n % 10, sum += x * x;
	return sum;
}

int happy(int n) {
	int nn;
	while (n > 999) n = dsum(n); /* 4 digit numbers can't cycle */
	nn = dsum(n);
	while (nn != n && nn != 1)
		n = dsum(n), nn = dsum(dsum(nn));

  //fix: original code seems to be wrong, expected output with nn instead of n
  //original code: return n == 1;
	return nn == 1;
}

EMSCRIPTEN_KEEPALIVE
int run_happynumbers(int cnt) {
	int i;
	for (i = 1; cnt /*|| !printf("\n")*/; i++)
		if (happy(i)) --cnt/*, printf("%d ", i)*/;
	return 0;
}
