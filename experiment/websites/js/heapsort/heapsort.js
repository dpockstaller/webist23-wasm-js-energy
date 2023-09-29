/* based on: https://rosettacode.org/wiki/Sorting_algorithms/Heapsort#JavaScript (2021-12-23) */

/**
 * @param {number[]} arr
 * @return {number[]}
 */
function heapsort(arr) {
  heapify(arr)
  end = arr.length - 1
  while (end > 0) {
    [arr[end], arr[0]] = [arr[0], arr[end]]
    end--
    siftDown(arr, 0, end)
  }
  return arr;
}

/**
 * @param {number[]} arr
 */
function heapify(arr) {
  start = Math.floor(arr.length/2) - 1

  while (start >= 0) {
    siftDown(arr, start, arr.length - 1)
    start--
  }
}

/**
 * @param {number[]} arr
 * @param {number} startPos
 * @param {number} endPos
 */
function siftDown(arr, startPos, endPos) {
  let rootPos = startPos

  while (rootPos * 2 + 1 <= endPos) {
    childPos = rootPos * 2 + 1
    if (childPos + 1 <= endPos && arr[childPos] < arr[childPos + 1]) {
      childPos++
    }
    if (arr[rootPos] < arr[childPos]) {
      [arr[rootPos], arr[childPos]] = [arr[childPos], arr[rootPos]]
      rootPos = childPos
    } else {
      return
    }
  }
}
