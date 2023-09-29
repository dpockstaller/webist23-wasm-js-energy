/* based on: https://rosettacode.org/wiki/Fibonacci_sequence#Recursive_33 (2021-12-30) */

/**
 * @param {number} n
 * @returns {number}
 */
function fibonacci(n) {
  return n<2?n:fibonacci(n-1)+fibonacci(n-2);
}
