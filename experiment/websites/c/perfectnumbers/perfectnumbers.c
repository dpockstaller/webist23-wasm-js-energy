/* based on: https://rosettacode.org/wiki/Perfect_numbers#C (2021-12-25) */

#include <math.h>
#include <emscripten/emscripten.h>

int perfectnumber(int n) {
    int max = (int)sqrt((double)n) + 1;
    int tot = 1;

    for (int i = 1; i < max; i++)
        if ( (n % i) == 0 ) {
            tot += i;
            int q = n / i;
            if (q > i)
                tot += q;
        }

    return tot == n;
}

EMSCRIPTEN_KEEPALIVE
int run_perfectnumbers(int max) {
    int cnt;
    for (int n = 2; n < max; n++)
        if (perfectnumber(n))
            cnt++;

    return cnt;
}
