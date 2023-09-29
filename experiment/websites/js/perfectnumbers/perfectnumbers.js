/* based on: https://rosettacode.org/wiki/Perfect_numbers#Imperative (2021-12-25) */

/**
 * @param {number} n
 * @returns {boolean}
 */
function perfectnumber(n)
{
  let sum = 1, sqrt = Math.floor(Math.sqrt(n));
  for (let i = sqrt-1; i>1; i--)
  {
    if (n % i === 0) {
      sum += i + n/i;
    }
  }
  if(n % sqrt === 0)
    sum += sqrt + (sqrt*sqrt === n ? 0 : n/sqrt);
  return sum === n;
}
