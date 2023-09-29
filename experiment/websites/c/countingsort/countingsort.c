/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Counting_sort#C (2021-12-23) */

#include <stdlib.h>
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
void countingsort(int *array, int n, int min, int max)
{
  int i, j, z;

  int range = max - min + 1;
  int *count = malloc(range * sizeof(*array));

  for(i = 0; i < range; i++) count[i] = 0;
  for(i = 0; i < n; i++) count[ array[i] - min ]++;

  for(i = min, z = 0; i <= max; i++) {
    for(j = 0; j < count[i - min]; j++) {
      array[z++] = i;
    }
  }

  free(count);
}

void min_max(int *array, int n, int *min, int *max)
{
  int i;

  *min = *max = array[0];
  for(i=1; i < n; i++) {
    if ( array[i] < *min ) {
      *min = array[i];
    } else if ( array[i] > *max ) {
      *max = array[i];
    }
  }
}
