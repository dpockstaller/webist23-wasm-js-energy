/* based on: https://rosettacode.org/wiki/Humble_numbers#C (2022-01-31) */

#include <emscripten/emscripten.h>

int isHumble(int i) {
    if (i <= 1) return 1;
    if (i % 2 == 0) return isHumble(i / 2);
    if (i % 3 == 0) return isHumble(i / 3);
    if (i % 5 == 0) return isHumble(i / 5);
    if (i % 7 == 0) return isHumble(i / 7);
    return 0;
}

EMSCRIPTEN_KEEPALIVE
int run_humblenumbers(int max) {
    int cnt;
    for (int n = 0; n < max; n++)
        if (isHumble(n))
            cnt++;

    return cnt;
}
