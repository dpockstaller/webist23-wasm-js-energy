/* based on: https://rosettacode.org/wiki/Towers_of_Hanoi#ES5 (2021-12-30) */

/**
 * @param {number} n
 * @param {number|string} a
 * @param {number|string} b
 * @param {number|string} c
 */
function move(n, a, b, c) {
  if (n > 0) {
    move(n-1, a, c, b);
    //console.log("Move disk from " + a + " to " + c);
    move(n-1, b, a, c);
  }
}
