/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Gnome_sort#JavaScript (2021-12-23) */

/**
 * @param {number[]} a
 * @returns {number[]}
 */
function gnomesort(a) {
  function moveBack(i) {
    for( ; i > 0 && a[i-1] > a[i]; i--) {
      var t = a[i];
      a[i] = a[i-1];
      a[i-1] = t;
    }
  }
  for (var i = 1; i < a.length; i++) {
    if (a[i-1] > a[i]) moveBack(i);
  }
  return a;
}
