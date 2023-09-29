/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Shell_sort#JavaScript (2021-12-23) */

/**
 * @param {number[]} a
 * @returns {number[]}
 */
function shellsort (a) {
  for (var h = a.length; h > 0; h = parseInt(h / 2)) {
    for (var i = h; i < a.length; i++) {
      var k = a[i];
      for (var j = i; j >= h && k < a[j - h]; j -= h)
        a[j] = a[j - h];
      a[j] = k;
    }
  }
  return a;
}
