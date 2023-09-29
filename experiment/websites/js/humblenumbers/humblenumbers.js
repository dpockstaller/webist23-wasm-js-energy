/* based on: https://rosettacode.org/wiki/Humble_numbers#C (2022-01-31) */

/**
 * @param {number} i
 * @returns {boolean}
 */
function isHumble(i) {
  if (i <= 1) return true;
  if (i % 2 === 0) return isHumble(i / 2);
  if (i % 3 === 0) return isHumble(i / 3);
  if (i % 5 === 0) return isHumble(i / 5);
  if (i % 7 === 0) return isHumble(i / 7);
  return false;
}
