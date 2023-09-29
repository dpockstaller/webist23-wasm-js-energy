/* based on: http://rosettacode.org/wiki/Sorting_algorithms/Bubble_sort#JavaScript (2021-12-24) */

/**
 * @param {number[]} values
 * @returns {number[]}
 */
function pancakesort(values) {
  for (let i = values.length - 1; i >= 1; i--) {
    // find the index of the largest element not yet sorted
    let max_idx = 0;
    let max = values[0];
    for (let j = 1; j <= i; j++) {
      if (values[j] > max) {
        max = values[j];
        max_idx = j;
      }
    }

    if (max_idx === i)
      continue; // element already in place

    let new_slice;

    // flip values max element to index 0
    if (max_idx > 0) {
      new_slice = values.slice(0, max_idx+1).reverse();
      for (let j = 0; j <= max_idx; j++)
        values[j] = new_slice[j];
    }

    // then flip the max element to its place
    new_slice = values.slice(0, i+1).reverse();
    for (let j = 0; j <= i; j++)
      values[j] = new_slice[j];
  }

  return values;
}
