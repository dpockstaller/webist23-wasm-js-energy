/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Merge_sort#JavaScript (2021-12-22) */

/**
 * @param {number[]} left
 * @param {number[]} right
 * @param {number[]} arr
 */
function merge(left, right, arr) {
  var a = 0;

  while (left.length && right.length) {
    arr[a++] = (right[0] < left[0]) ? right.shift() : left.shift();
  }
  while (left.length) {
    arr[a++] = left.shift();
  }
  while (right.length) {
    arr[a++] = right.shift();
  }
}

/**
 * @param {number[]} arr
 * @returns {number[]}
 */
function mergesort(arr) {
  var len = arr.length;

  if (len === 1) { return; }

  var mid = Math.floor(len / 2),
    left = arr.slice(0, mid),
    right = arr.slice(mid);

  mergesort(left);
  mergesort(right);
  merge(left, right, arr);
  return arr;
}
