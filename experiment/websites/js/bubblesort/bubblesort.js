/* based on: http://rosettacode.org/wiki/Sorting_algorithms/Bubble_sort#JavaScript (2021-12-20) */

/**
 * @param {number[]} values
 * @returns {number[]}
 */
function bubble_sort(values) {
  var done = false;
  while (!done) {
    done = true;
    for (var i = 1; i<values.length; i++) {
      if (values[i-1] > values[i]) {
        done = false;
        [values[i-1], values[i]] = [values[i], values[i-1]]
      }
    }
  }
  return values;
}
