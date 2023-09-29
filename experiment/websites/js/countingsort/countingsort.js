/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Counting_sort#JavaScript (2021-12-23) */

/**
 * @param {number[]} arr
 * @param {number} min
 * @param {number} max
 * @returns {number[]}
 */
var countingsort = function(arr, min, max) {
  var i, z = 0, count = [];

  for (i = min; i <= max; i++) {
    count[i] = 0;
  }

  for (i=0; i < arr.length; i++) {
    count[arr[i]]++;
  }

  for (i = min; i <= max; i++) {
    while (count[i]-- > 0) {
      arr[z++] = i;
    }
  }
  return arr;
}
