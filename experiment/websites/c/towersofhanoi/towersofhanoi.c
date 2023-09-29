/* based on: https://rosettacode.org/wiki/Towers_of_Hanoi#C (2021-12-30) */

#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void move(int n, int from, int via, int to)
{
  if (n > 1) {
    move(n - 1, from, to, via);
    move(n - 1, via, from, to);
  }
}
