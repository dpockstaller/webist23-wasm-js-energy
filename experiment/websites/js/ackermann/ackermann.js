/* based on: https://rosettacode.org/wiki/Ackermann_function#ES5 (2022-01-14) */

/**
 * @param {number} m
 * @param {number} n
 * @returns {number}
 */
function ack(m, n) {
  return m === 0 ? n + 1 : ack(m - 1, n === 0  ? 1 : ack(m, n - 1));
}
