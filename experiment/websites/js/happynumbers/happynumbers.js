/* based on: https://rosettacode.org/wiki/Happy_numbers#JavaScript (2021-12-24) */

/**
 * @param {number} number
 * @returns {number}
 */
function happy(number) {
  var m, digit ;
  var cycle = [] ;

  while(number !== 1 && cycle[number] !== true) {
    cycle[number] = true ;
    m = 0 ;
    while (number > 0) {
      digit = number % 10 ;
      m += digit * digit ;
      number = (number  - digit) / 10 ;
    }
    number = m ;
  }
  return (number === 1) ;
}
